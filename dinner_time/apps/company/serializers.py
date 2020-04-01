from rest_framework import serializers

from apps.company.models import ReferralLink
from apps.users.models import User


class CreateCompanySerializer(serializers.ModelSerializer):
    """
    A serializer for create company in admin panel
    """

    class Meta:
        model = User
        fields = (
            'id', 'email', 'company_name', 'create_date', 'is_company')

    def create_ref_link_for_update_auth_data(self, obj):
        link = ReferralLink.objects.create(user=obj, upid=ReferralLink.get_generate_upid())
        return link.upid


class ChangeRegAuthDataSerializer(serializers.ModelSerializer):
    """
    A serializer for update username and password when clicking on the registration link
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')
