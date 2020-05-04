from collections import OrderedDict, Mapping
from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField, set_value
from rest_framework.relations import PKOnlyObject
from rest_framework.settings import api_settings

from apps.users.models import Tariff

User = get_user_model()


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ['id', 'name', 'max_cost_day', 'description']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for create user
    """
    phone = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    def validate_phone(self, value):
        phone = PhoneNumber.from_string(phone_number=value, region='RU').as_e164
        return phone

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'tariff', 'phone', 'email', 'department']


class UserSerializer(serializers.ModelSerializer):
    """
    Main user serializer for get information
    """
    tariff = TariffSerializer()

    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'first_name',
                  'last_name', 'middle_name', 'phone', 'email', 'tariff', 'department', 'email_verified', 'is_blocked',
                  'block_date', 'company_data', 'create_date', 'update_date', 'lft', 'rght', 'tree_id', 'level',
                  'parent', 'groups', 'user_permissions']


class UserChangeSerializer(serializers.ModelSerializer):
    """
    Serializer for change information
    """

    def to_internal_value(self, data):
        """
        List of dicts of native values <- List of dicts of primitive datatypes.
        """
        if not isinstance(data, Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')

        ret = OrderedDict()
        errors = OrderedDict()
        fields = self._writable_fields

        for field in fields:
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            primitive_value = field.get_value(data)
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except ValidationError as exc:
                errors[field.field_name] = exc.detail
            except SkipField:
                pass
            else:
                set_value(ret, field.source_attrs, validated_value)

        if errors:
            raise ValidationError(errors)

        if data.get('is_blocked'):
            ret["block_date"] = datetime.now(pytz.timezone(settings.TIME_ZONE))
        else:
            ret["block_date"] = None

        return ret

    def to_representation(self, data):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(data)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'tariff', 'email', 'department', 'is_blocked']


class EmptySerializer(serializers.Serializer):
    pass
