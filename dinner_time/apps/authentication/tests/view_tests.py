import json

import pytest
from django.urls import reverse

from apps.users.models import User
from apps.users.utils import create_user_account


@pytest.mark.django_db
class TestAuthenticationView:
    def create_user(self):
        phone = '89313147222'
        user = User.objects.filter(phone=phone)

        if not user.exists():
            create_user_account(phone=phone, first_name='Тест', last_name="Тестовов",
                                email='test@protonmail.com', password='test', username='test')

    def get_authentication(self, client, username='89313147222', password='test'):
        url = reverse('AUTHENTICATION:authentication-login')
        self.create_user()

        data = {
            'username': username,
            'password': password,
        }
        request = client.post(url, data=data, content_type='application/json')
        user_data = json.loads(request.content)

        return request, user_data

    def test_login(self, client):
        request, user_data = self.get_authentication(client)
        email = user_data['email']

        assert request.status_code == 200
        assert email == 'test@protonmail.com'

    def test_logout(self, client):
        response, user_data = self.get_authentication(client)
        url = reverse('AUTHENTICATION:authentication-logout')
        request = client.get(path=url, HTTP_AUTHORIZATION=f'Token {user_data["auth_token"]}')
        response_logout = json.loads(request.content)

        assert request.status_code == 200
        assert response_logout['success'] == 'Успешный выход из системы'

    def test_change_password(self, client):
        response, user_data = self.get_authentication(client)
        url = reverse('AUTHENTICATION:authentication-password-change')
        data = {
            'current_password': 'test',
            'new_password': 'TEST',
        }

        request = client.put(url, data=data, content_type='application/json',
                             HTTP_AUTHORIZATION=f'Token {user_data["auth_token"]}')

        assert request.status_code == 202

    def test_error_change_password(self, client):
        response, user_data = self.get_authentication(client)
        url = reverse('AUTHENTICATION:authentication-password-change')
        data = {
            'current_password': 'abrakadabra',
            'new_password': 'TEST',
        }

        request = client.put(url, data=data, content_type='application/json',
                             HTTP_AUTHORIZATION=f'Token {user_data["auth_token"]}')
        response_change_password = json.loads(request.content)

        assert request.status_code == 400
        assert response_change_password['current_password'][0] == 'Текущий пароль не совпадает'

    def test_error_login_username(self, client):
        request, invalid_username = self.get_authentication(client, username='hello_people@mail.ru', password='TEST')

        assert request.status_code == 400
        assert invalid_username[0] == "Некорректные учётные данные. Пожалуйста, попробуйте ещё раз"

    def test_error_login_password(self, client):
        request, invalid_password = self.get_authentication(client, password='abrakadabra')

        assert request.status_code == 400
        assert invalid_password[0] == "Некорректные учётные данные. Пожалуйста, попробуйте ещё раз"
