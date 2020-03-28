from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'username', 'is_staff', 'is_active', 'date_joined', 'first_name',
                  'last_name', 'middle_name', 'phone', 'email', 'email_verified', 'is_blocked', 'block_date',
                  'is_removed', 'removed_date', 'create_date', 'update_date', 'lft', 'rght', 'tree_id', 'level',
                  'parent', 'groups', 'user_permissions']
