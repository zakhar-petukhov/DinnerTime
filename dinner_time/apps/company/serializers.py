from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers

from apps.company.models import Department, Company
from apps.users.models import User
from apps.users.serializers import UserSerializer


class CompanyDetailSerializer(serializers.ModelSerializer):
    """
    A serializer for get all information about company
    """

    class Meta:
        model = Company
        fields = (
            'id', 'company_name', 'full_address', 'inn', 'kpp', 'ogrn', 'registration_date', 'bank_name',
            'bik', 'corporate_account', 'settlement_account')


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for department. Used how main serializer and for create department.
    """

    total_number_users = serializers.SerializerMethodField('get_total_number_users')

    def get_total_number_users(self, obj):
        return User.objects.filter(company_data=Company.objects.get(company_department=obj.id)).count()

    class Meta:
        model = Department
        fields = ['id', 'name', 'company', 'total_number_users']


class CompanyGetSerializer(serializers.ModelSerializer):
    """
    A serializer for get all company
    """

    all_person = serializers.SerializerMethodField('get_all_person', label='Все сотрудники')
    count_person = serializers.SerializerMethodField('get_count_person', label='Количество сотрудников')
    department = serializers.SerializerMethodField('get_all_department', label='Все отделы')
    company_data = CompanyDetailSerializer(required=False)

    def get_count_person(self, obj):
        return User.objects.filter(parent=obj.id).count()

    def get_all_person(self, obj):
        qs = User.objects.filter(parent=obj.id)
        serializer = UserSerializer(instance=qs, many=True)
        return serializer.data

    def get_all_department(self, obj):
        qs = Department.objects.filter(company_id=obj.company_data.id)
        serializer = DepartmentSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ['id', 'company_data', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'is_blocked',
                  'count_person', 'all_person', 'department', 'is_active']


class CompanyCreateSerializer(serializers.ModelSerializer):
    """
    A serializer for create company
    """

    phone = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    company_data = CompanyDetailSerializer(required=False)

    def validate_phone(self, value):
        phone = PhoneNumber.from_string(phone_number=value, region='RU').as_e164
        return phone

    class Meta:
        model = User
        fields = ['id', 'company_data', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'is_blocked',
                  'is_active']
