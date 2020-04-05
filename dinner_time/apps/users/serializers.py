from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.models import Department

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Main user serializer for get information
    """

    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'username', 'is_staff', 'is_active', 'date_joined', 'first_name',
                  'last_name', 'middle_name', 'phone', 'email', 'email_verified', 'department', 'is_blocked',
                  'block_date', 'create_date', 'update_date', 'lft', 'rght', 'tree_id', 'level', 'parent', 'groups',
                  'user_permissions']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for create user
    """

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'department']


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for department. Used how main serializer and for create department.
    """
    total_number_users = serializers.SerializerMethodField('get_total_number_users')

    def get_total_number_users(self, obj):
        return len(User.objects.filter(department=obj.id))

    class Meta:
        model = Department
        fields = ['id', 'name', 'company', 'total_number_users']


class EmptySerializer(serializers.Serializer):
    pass
