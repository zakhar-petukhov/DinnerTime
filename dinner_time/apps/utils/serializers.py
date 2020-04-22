from rest_framework import serializers

from apps.utils.models import Settings


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['id', 'close_order_time', 'enabled']
