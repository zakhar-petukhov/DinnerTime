import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUserView:
    def test_user_change_information(self, api_client, get_token_user, get_token_company):
        token_company, company = get_token_company
        token_user, user = get_token_user
        url = reverse('USERS:user-detail', kwargs={'pk': user.id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "first_name": "Пупкин",
            "is_blocked": True
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 200
        user_data['first_name'] = 'Пупкин'
        user_data['is_blocked'] = True

    def test_user_get_detail_information(self, api_client, get_token_user):
        token_user, user = get_token_user
        url = reverse('USERS:user-detail-information', kwargs={"pk": user.id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        assert user_data['first_name'] == 'Тест'

    def test_create_tariff(self, api_client, get_token_user):
        token_user, user = get_token_user
        url = reverse('USERS:create_tariff')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        data = {
            "name": "Лайт",
            "max_cost_day": 300,
            "description": "Тупа чтобы шашлыка навернуть"
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 201
        assert user_data['name'] == 'Лайт'

    def test_change_tariff(self, api_client, get_token_user, create_tariff):
        token_user, user = get_token_user
        url = reverse('USERS:change_tariff', kwargs={"tariff_id": create_tariff().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        data = {
            "max_cost_day": 500
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 200
        assert user_data['max_cost_day'] == 500

    def test_get_all_tariff(self, api_client, get_token_user, create_tariff):
        create_tariff()
        token_user, user = get_token_user
        url = reverse('USERS:list_all_tariff')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_user.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        assert user_data[0]['name'] == "Лайт"
