import uuid

from django.contrib.auth import authenticate, get_user_model, user_logged_out
from django.utils.translation import LANGUAGE_SESSION_KEY
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.models import User


def get_and_authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise serializers.ValidationError("Некорректные учётные данные. Пожалуйста, попробуйте ещё раз")

    return user


def create_user_account(email, first_name="", last_name="", parent=None, **extra_fields):
    phone_number = extra_fields.get('phone')
    if phone_number:
        phone = User().get_phone_number(phone=phone_number)
        extra_fields['phone'] = phone

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
