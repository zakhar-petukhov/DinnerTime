from django.core.exceptions import ImproperlyConfigured
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.authentication.utils import logout
from apps.users.serializers import EmptySerializer
from apps.utils.models import ReferralLink
from .serializers import *
from .utils import get_and_authenticate_user, create_user_account


class AuthViewSet(GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
        'signup': UserSignUpSerializer,
        'password_change': PasswordChangeSerializer,
    }

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        AuthUserSerializer(user).get_auth_token(user)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def logout(self, request):
        logout(request)
        data = {'success': 'Успешный выход из системы'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class UserChangeRegAuthDataView(UpdateAPIView):
    serializer_class = ChangeRegAuthDataSerializer
    model = User
    permission_classes = ()

    def get_object(self):
        upid = self.kwargs["referral_upid"]
        obj = get_object_or_404(ReferralLink, upid=upid, is_active=True)

        return obj

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if User.objects.filter(username=serializer.data.get("username")).exists():
                raise serializers.ValidationError(
                    "Такой username уже занят, пожалуйста, введите другой и повторите запрос.")

            obj.user.set_password(serializer.data.get("password"))
            obj.is_active = False
            obj.user.save()
            obj.save()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
