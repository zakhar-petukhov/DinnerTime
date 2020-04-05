from rest_framework import serializers

from apps.users.models import User


class GetInformationCompanySerializer(serializers.ModelSerializer):
    """
    A serializer for get all information about company
    """

    class Meta:
        model = User
        fields = ['id', 'company_name', 'first_name', 'last_name', 'middle_name', 'phone', 'email', 'is_blocked']


class CreateCompanySerializer(serializers.ModelSerializer):
    """
    A serializer for create company in admin panel
    """

    class Meta:
        model = User
        fields = (
            'id', 'email', 'company_name', 'create_date', 'is_company')


class ChangeRegAuthDataSerializer(serializers.ModelSerializer):
    """
    A serializer for update username and password when clicking on the registration link
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone', 'username', 'password')
