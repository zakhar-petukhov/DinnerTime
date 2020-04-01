from rest_framework import serializers

from apps.users.models import User
from apps.company.models import ReferralLink


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'company_name', 'create_date')

    def create_ref_link_for_update_auth_data(self, obj):
        link = ReferralLink.objects.create(user=obj, upid=ReferralLink.get_generate_upid())
        return link.upid

