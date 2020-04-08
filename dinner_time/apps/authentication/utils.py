import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth import user_logged_out
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import LANGUAGE_SESSION_KEY
from phonenumbers import NumberParseException
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.company.models import Company
from apps.users.models import User
from apps.utils.models import ReferralLink


def get_and_authenticate_user(password, username=None):
    auth = CustomAuthenticationBackend()
    user = auth.authenticate(email_or_phone=username, password=password)
    if user is None:
        raise serializers.ValidationError("Некорректные учётные данные. Пожалуйста, попробуйте ещё раз")

    return user


def create_user_account(email, first_name="", last_name="", parent=None, **extra_fields):
    phone_number = extra_fields.get('phone')
    company_data = extra_fields.get('company_data')

    if phone_number:
        phone = User().get_phone_number(phone=phone_number)
        extra_fields['phone'] = phone

    if company_data:
        company = Company.objects.create(**company_data)
        extra_fields['company_data'] = company

    user = get_user_model().objects.create_user(
        email=email, first_name=first_name, last_name=last_name, parent=parent, **extra_fields)
    return user


def logout(request):
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if not getattr(user, 'is_authenticated', True):
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)
    Token.objects.get(user=user).delete()

    # remember language choice saved to session
    language = request.session.get(LANGUAGE_SESSION_KEY)

    request.session.flush()

    if language is not None:
        request.session[LANGUAGE_SESSION_KEY] = language

    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()


def generate_random_password():
    return {
        'password': uuid.uuid4().hex[:30]
    }


def create_ref_link_for_update_auth_data(obj):
    link = ReferralLink.objects.create(user=obj, upid=ReferralLink.get_generate_upid())
    return link.upid


class CustomAuthenticationBackend:
    def authenticate(self, email_or_phone=None, password=None):
        try:
            email_or_phone = self.get_valid_phone(email_or_phone)

            user = User.objects.get(
                Q(email=email_or_phone) | Q(phone=email_or_phone)
            )
            pwd_valid = user.check_password(password)
            if pwd_valid:
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_valid_phone(self, email_or_phone):
        try:
            email_or_phone = User().get_phone_number(email_or_phone)
            return email_or_phone
        except NumberParseException:
            return email_or_phone
