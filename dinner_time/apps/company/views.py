from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser

from apps.authentication.utils import create_user_account, generate_random_username_password, \
    create_ref_link_for_update_auth_data
from apps.company.serializers import *
from apps.users.models import User
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
        serializer.validated_data.update(generate_random_username_password())
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
        '200': openapi.Response('Успешно', CompanySerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class AllCompaniesView(ListAPIView):
    queryset = User.objects.filter(company_data__isnull=False)
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_data__company_name']
    permission_classes = [IsAdminUser]


@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_summary='Блокировка или разблокировка компании',
    request_body=CompanyBlockSerializer,
    responses={
        '200': openapi.Response('Успешно', CompanySerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class CompanyUpdateBlockView(UpdateAPIView):
    serializer_class = CompanyBlockSerializer
    model = User
    permission_classes = [IsAdminUser]

    def get_object(self):
        company_id = self.kwargs.get("company_id")
        obj = get_object_or_404(User, company_data=company_id)

        return obj


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Детальный просмотр одной компании.',
    operation_description='''Есть возможность полностью посмотореть данные о компании \
(сколько человек, какие созданы отделы)''',
    responses={
        '200': openapi.Response('Успешно', CompanySerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class CompanyDetailView(ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        return User.objects.filter(company_data=company_id)
