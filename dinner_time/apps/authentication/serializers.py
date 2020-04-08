from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.models import User


class UserLoginSerializer(serializers.Serializer):
    """
    A user serializer for login the user
    """

    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    """
    A user serializer for authentication the user
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')

    def get_auth_token(self, obj):
        token, create = Token.objects.get_or_create(user=obj)
        return token.key


class UserSignUpSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """
    A user serializer for change password
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Текущий пароль не совпадает')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class ChangeRegAuthDataSerializer(serializers.ModelSerializer):
    """
    A serializer for update username and password when clicking on the registration link
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise serializers.ValidationError(
                "Такой username уже занят, пожалуйста, введите другой и повторите запрос.")
        return username

    def validate_phone(self, phone_number):
        phone = User().get_phone_number(phone_number)
        return phone

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone', 'username', 'password', 'email_verified')
