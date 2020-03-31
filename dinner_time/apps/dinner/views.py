from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.dinner.models import Menu
from apps.dinner.serializers import MenuSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description='Получение списка меню',
    operation_summary='Меню',
    responses={
        '200': MenuSerializer(many=True),
        '400': 'Неверный формат запроса'
    }
)
                  )
class MenuView(ListAPIView):
    queryset = Menu.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = (DjangoFilterBackend,)
    serializer_class = MenuSerializer
