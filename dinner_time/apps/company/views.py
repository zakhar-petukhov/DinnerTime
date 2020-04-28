from datetime import datetime

import pytz
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.company.serializers import *
from apps.company.serializers import DepartmentSerializer
from apps.users.models import User
from apps.users.permissions import IsCompanyAuthenticated
from apps.users.serializers import UserCreateSerializer, EmptySerializer
from apps.users.utils import *
from apps.utils.func_for_send_message import send_message_for_change_auth_data_client
from apps.utils.func_for_send_message import send_message_for_change_auth_data_company


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Создание компании',
    responses={
        '201': openapi.Response('Создано', CompanyCreateSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class CreateCompanyView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CompanyCreateSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update(generate_random_password_username())
        company = create_user_account(**serializer.validated_data)

        upid = create_ref_link_for_update_auth_data(obj=company)
        headers = self.get_success_headers(serializer.data)

        url = settings.URL_FOR_CHANGE_AUTH_DATA.format(upid)
        header, body = send_message_for_change_auth_data_company(url=url,
                                                                 company_name=serializer.data['company_data'].get(
                                                                     'company_name'))
        email = EmailMessage(header, body, to=[serializer.data.get('email')])
        email.send()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Просмотр всех компаний',
    operation_description='Просмотр всех компаний. Есть возможность отфильтровать по названию',
    responses={
        '200': openapi.Response('Успешно', CompanyGetSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class AllCompaniesView(ListAPIView):
    queryset = User.objects.filter(company_data__isnull=False, is_active=True)
    serializer_class = CompanyGetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_data__company_name']
    permission_classes = [IsAdminUser]


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Детальный просмотр одной компании.',
    operation_description='''Есть возможность полностью посмотореть данные о компании \
(сколько человек, какие созданы отделы)''',
    responses={
        '200': openapi.Response('Успешно', CompanyGetSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class CompanyDetailView(ListAPIView):
    serializer_class = CompanyGetSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        return User.objects.filter(id=company_id, company_data__isnull=False)


@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_summary='Обновление данных компании',
    operation_description='''
Можем производить все манипуляции с компанией:
1) Обновление любого поля менеджера компании
2) Обновление любого поля самой компании
3) Блокировка компании {"is_block": true} ---> {"is_block": false}
4) Удаление компании {"is_active": false} - компания переводится в статус неактивна, но из базы данных не удаляется
''',
    request_body=CompanyGetSerializer,
    responses={
        '200': openapi.Response('Успешно', CompanyGetSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class CompanyChangeDetailView(UpdateAPIView):
    serializer_class = CompanyGetSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        company_id = self.kwargs.get("company_id")
        return get_object_or_404(User, id=company_id, company_data__isnull=False)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        company_data = request.data.pop('company_data', None)
        is_blocked = request.data.pop('is_blocked', None)

        if company_data:
            Company.objects.filter(company_user=instance).update(**company_data)

        if is_blocked in [True, False]:
            instance.is_blocked = is_blocked
            instance.block_date = datetime.now(pytz.timezone(settings.TIME_ZONE)) if is_blocked else None
            instance.save()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


@method_decorator(name='create_department', decorator=swagger_auto_schema(
    operation_summary='Создание отдела',
    responses={
        '201': openapi.Response('Создано', DepartmentSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='add_user', decorator=swagger_auto_schema(
    operation_summary='Добавление сотрудников в отделы',
    operation_description='''Создается сотрудник и добавляется в отдел. 
Сотруднику генерируется базовый логин и пароль и отправляется на почту сообщение о смене, после перехода по \
уникальной ссылке, сотрудник ставит свой логин и пароль''',
    responses={
        '202': openapi.Response('Изменено', UserCreateSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Просмотр всех отделов',
    operation_description='Показываются все отделы вместе с количеством сотрудников',
    responses={
        '200': openapi.Response('Успешно', DepartmentSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class DepartmentViewSet(GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsCompanyAuthenticated]
    serializer_class = EmptySerializer
    serializer_classes = {
        'create_department': DepartmentSerializer,
        'add_user': UserCreateSerializer,
        'list': DepartmentSerializer,
    }

    # Create department
    @action(methods=['POST'], detail=False)
    def create_department(self, request, *args, **kwargs):
        company = get_object_or_404(User, id=request.user.id, company_data__isnull=False)
        request.data['company'] = company.company_data.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Create, add user into department and send message for change password, and login on the mail
    @action(methods=['POST'], detail=False)
    def add_user(self, request):
        parent = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update(generate_random_password_username())

        user = create_user_account(parent=parent, **serializer.validated_data)
        upid = create_ref_link_for_update_auth_data(obj=user)

        url = settings.URL_FOR_CHANGE_AUTH_DATA.format(upid)
        header, body = send_message_for_change_auth_data_client(url=url,
                                                                company_name=parent.company_data.company_name)
        email = EmailMessage(header, body, to=[serializer.data.get('email')])
        email.send()

        return Response(status=status.HTTP_202_ACCEPTED)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_object(self):
        departament_id = self.kwargs["pk"]
        obj = get_object_or_404(Department, pk=departament_id)
        return obj

    def get_queryset(self):
        employee_id = self.request.user.id
        return Department.objects.filter(company_id__company_user=User.objects.get(id=employee_id))
