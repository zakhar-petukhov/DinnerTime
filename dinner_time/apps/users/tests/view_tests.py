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
