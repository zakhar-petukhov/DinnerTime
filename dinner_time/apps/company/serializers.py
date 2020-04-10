from rest_framework import serializers

from apps.company.models import Department, Company
from apps.users.models import User
from apps.users.serializers import DepartmentSerializer, UserSerializer


class CompanyDetailSerializer(serializers.ModelSerializer):
    """
    A serializer for get all information about company
    """

    class Meta:
        model = Company
        fields = (
            'id', 'company_name', 'full_address', 'inn', 'kpp', 'ogrn', 'registration_date', 'bank_name',
            'bik', 'corporate_account', 'settlement_account')


class CompanySerializer(serializers.ModelSerializer):
    """
    Main serializer for company
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

    def validate_phone(self, phone_number):
        phone = User().get_phone_number(phone_number)
        return phone

    class Meta:
        model = User
        fields = ['id', 'company_data', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'is_blocked',
                  'count_person', 'all_person', 'department', 'is_active']
