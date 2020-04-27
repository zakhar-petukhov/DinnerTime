import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def get_or_create_token(db, create_user):
    user = create_user(phone='89313147222', first_name='Тест', last_name="Тестовов",
                       email='test@protonmail.com', username='test', password='test', is_superuser=True,
                       is_staff=True)
    token, _ = Token.objects.get_or_create(user=user)
    return token
