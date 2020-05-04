from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.company.utils import send_message
from apps.dinner.data_for_swagger import request_for_create_dinner
from apps.dinner.models import Dinner
from apps.dinner.serializers import DinnerSerializer
from apps.users.data_for_swagger import request_invite_users
from apps.users.permissions import IsCompanyAuthenticated
from apps.users.serializers import *
from apps.users.utils import *

User = get_user_model()


@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Изменение информации о сотруднике',
    operation_description='Только менеджер компании может менять информацию о сотруднике',
    responses={
        '200': openapi.Response('Успешно', UserChangeSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='detail_information', decorator=swagger_auto_schema(
    operation_summary='Детальный просмотр одного сотрудника',
    operation_description='Сотрудник может посмотреть всю информацию о себе',
    responses={
        '200': openapi.Response('Успешно', UserSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class UserViewSet(GenericViewSet, mixins.UpdateModelMixin):
    permission_classes = [IsCompanyAuthenticated, ]
    queryset = ()
    serializer_class = EmptySerializer
    serializer_classes = {
        'detail_information': UserSerializer,
        'update': UserChangeSerializer,
    }

    # Client can view information about themselves
    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated, ])
    def detail_information(self, request, *args, **kwargs):
        queryset = User.objects.get(id=self.kwargs.get("pk"))
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        user_id = self.kwargs.get("pk")
        return get_object_or_404(User, id=user_id)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание обеда',
    request_body=request_for_create_dinner,
    responses={
        '201': openapi.Response('Создано', DinnerSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class UserCreateDinnerView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Dinner.objects.all()
    serializer_class = DinnerSerializer

    def get_object(self):
        return get_object_or_404(Dinner, id=self.kwargs.get("dish_id"))


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Все доступные тарифы.',
    responses={
        '200': openapi.Response('Успешно', TariffSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Изменение тарифа.',
    responses={
        '200': openapi.Response('Успешно.', TariffSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание тарифа.',
    request_body=TariffSerializer,
    responses={
        '201': openapi.Response('Создано', TariffSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class TariffCreateView(ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Tariff, id=self.kwargs.get("tariff_id"))


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Приглашение работников от имени компании.',
    request_body=request_invite_users,
    responses={
        '201': openapi.Response('Создано'),
        '400': 'Неверный формат запроса'
    }
)
                  )
class InviteUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form_data = request.data

        tariff = form_data.pop('tariff')
        parent = request.user

        for employee in form_data['emails']:
            employee['tariff'] = Tariff.objects.get(pk=tariff)
            employee.update(generate_random_password_username())
            user = create_user_account(parent=parent, **employee)
            upid = create_ref_link_for_update_auth_data(obj=user)
            send_message(company_name=parent.company_data.company_name, upid=upid, data=employee)

        return HttpResponse(status=status.HTTP_201_CREATED)
