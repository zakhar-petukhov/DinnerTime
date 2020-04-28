from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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
