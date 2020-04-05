from datetime import datetime

import pytz
from django.conf import settings
from rest_framework import serializers

from apps.users.models import User, Department
from users.serializers import DepartmentSerializer


class CompanySerializer(serializers.ModelSerializer):
    """
    A serializer for get all information about company
    """

    class Meta:
        model = User
        fields = ['id', 'company_name', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'is_blocked']


class CompanyBlockSerializer(serializers.ModelSerializer):
    """
    A serializer which blocks or unlocks the company
    """

    is_blocked = serializers.BooleanField(initial=False, label='Заблокирован')
    block_date = serializers.SerializerMethodField('get_block_date', label='Дата блокировки')

    def get_block_date(self, obj):
        if obj.is_blocked:
            return datetime.now(pytz.timezone(settings.TIME_ZONE))
        return None

    class Meta:
        model = User
        fields = ['is_blocked', 'block_date']


class CompanyCreateSerializer(serializers.ModelSerializer):
    """
    A serializer for create company in admin panel
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'company_name', 'create_date', 'is_company')


class CompanyDetailSerializer(serializers.ModelSerializer):
    """
    A serializer for get detail information about company
    """

    department = serializers.SerializerMethodField('get_all_department', label='Все отделы')
    all_person = serializers.SerializerMethodField('get_all_person', label='Все сотрудники')

    def get_all_department(self, obj):
        qs = Department.objects.filter(company_id=obj.id)
        serializer = DepartmentSerializer(instance=qs, many=True)
        return serializer.data

    def get_all_person(self, obj):
        return len(User.objects.filter(parent=obj.id))

    class Meta:
        model = User
        fields = (
            'id', 'company_name', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'is_blocked',
            'department', 'all_person')
