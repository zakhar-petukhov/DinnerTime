import phonenumbers
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.models import Department

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    A user serializer for get information
    """
    phone = serializers.SerializerMethodField('get_phone_number')

    def get_phone_number(self, obj):
        phone_number = phonenumbers.parse(obj.phone, "RU")
        return f"+{str(phone_number.country_code) + str(phone_number.national_number)}"

    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'username', 'is_staff', 'is_active', 'date_joined', 'first_name',
                  'last_name', 'middle_name', 'phone', 'email', 'email_verified', 'employee_department', 'is_blocked',
                  'block_date', 'create_date', 'update_date', 'lft', 'rght', 'tree_id', 'level', 'parent', 'groups',
                  'user_permissions']


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for department. Used how main serializer and for create department.
    """
    name = serializers.CharField(required=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'employee']


class DepartmentUpdateUserSerializer(DepartmentSerializer):
    """
    Update department (add, delete employee)
    """
    employee = UserSerializer(many=True)


class DepartmentGetSerializer(DepartmentSerializer):
    """
    Get all information about department
    """

    employee = serializers.SerializerMethodField('get_total_number_users')

    def get_total_number_users(self, obj):
        return len(Department.objects.filter(employee_id=obj.id))


class EmptySerializer(serializers.Serializer):
    pass
