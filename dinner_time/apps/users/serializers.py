from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.models import Department

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'username', 'is_staff', 'is_active', 'date_joined', 'first_name',
                  'last_name', 'middle_name', 'phone', 'email', 'email_verified', 'is_blocked', 'block_date',
                  'create_date', 'update_date', 'lft', 'rght', 'tree_id', 'level',
                  'parent', 'groups', 'user_permissions']


class DepartmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    employee = UserSerializer(many=True, required=False)

    class Meta:
        model = Department
        fields = ['id', 'name', 'employee']


class EmptySerializer(serializers.Serializer):
    pass
