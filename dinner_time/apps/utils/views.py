from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from apps.dinner.serializers import *


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Все настройки.',
    responses={
        '201': openapi.Response('Успешно', SettingsSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление настройки.',
    request_body=SettingsSerializer,
    responses={
        '201': openapi.Response('Успешно', SettingsSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class SettingsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
