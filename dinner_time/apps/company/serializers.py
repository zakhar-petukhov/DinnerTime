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

    all_person = serializers.SerializerMethodField('get_all_person', label='Все сотрудники')
    department = serializers.SerializerMethodField('get_all_department', label='Все отделы')

    def get_all_person(self, obj):
        return len(User.objects.filter(parent=obj.id))

    def get_all_department(self, obj):
        qs = Department.objects.filter(company_id=obj.id)
        serializer = DepartmentSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ['id', 'company_name', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'is_blocked',
                  'all_person', 'department']


class CompanyBlockSerializer(serializers.ModelSerializer):
    """
    A serializer which blocks or unlocks the company
    """

    def to_representation(self, obj):
        inf = {
            "is_blocked": obj.is_blocked,
            "block_date": obj.block_date
        }

        return inf

    def to_internal_value(self, data):
        if data.get('is_blocked'):
            return {
                "is_blocked": data.get('is_blocked'),
                "block_date": datetime.now(pytz.timezone(settings.TIME_ZONE)),
            }

        return {
            "is_blocked": data.get('is_blocked'),
            "block_date": None,
        }

    class Meta:
        model = User
        fields = ['is_blocked']


class CompanyCreateSerializer(serializers.ModelSerializer):
    """
    A serializer for create company in admin panel
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'company_name', 'create_date', 'is_company')
