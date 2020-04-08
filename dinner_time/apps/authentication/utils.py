import uuid

from django.contrib.auth import authenticate, get_user_model, user_logged_out
from django.utils.translation import LANGUAGE_SESSION_KEY
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.models import User
from apps.utils.models import ReferralLink
from apps.company.models import Company


def get_and_authenticate_user(username, password):
    user = authenticate(username=username, password=password)
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


def generate_random_username_password():
    return {
        'username': uuid.uuid4().hex[:20],
        'password': uuid.uuid4().hex[:30]
    }


def create_ref_link_for_update_auth_data(obj):
    link = ReferralLink.objects.create(user=obj, upid=ReferralLink.get_generate_upid())
    return link.upid
