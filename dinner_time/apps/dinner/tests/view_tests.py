import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDinnerView:
    def test_create_category_dish(self, api_client, get_token_company):
        token_company, company = get_token_company
        url = reverse('DINNER:create_dish_category')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "name": "Вторые блюда"
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 201
        user_data['name'] = 'Вторые блюда'

    def test_create_dish(self, api_client, get_token_company, create_category_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:create_dish_category')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "name": "Гороховый суп",
            "cost": 90,
            "weight": 120,
            "composition": "Вода, горох",
            "category_dish": create_category_dish().id
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 201
        user_data['name'] = 'Гороховый суп'

    def test_create_complex_dinner(self, api_client, get_token_company, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:create_complex_dinner')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "name": "Комплексный обед №2",
            "dishes": [
                {
                    "id": create_dish().id,
                }
            ]
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)

        assert response.status_code == 201
        user_data['name'] = 'Комплексный обед №2'

    def test_create_menu(self, api_client, get_token_company, create_dish, create_complex_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:create_menu')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "dish": [
                {
                    "id": create_dish().id
                }
            ],
            "complex_dinner": [
                {
                    "id": create_complex_dish().id
                }
            ],
            "available_order_date": "2020-05-01"
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')

        assert response.status_code == 201

    def test_get_detail_information_for_complex_dinner(self, api_client, get_token_company, create_complex_dish):
        create_complex_dish()
        token_company, company = get_token_company
        url = reverse('DINNER:detail_complex_dinner', kwargs={"complex_id": create_complex_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        user_data[0]['name'] = 'Комплексный обед №2'

    def test_get_list_all_category(self, api_client, get_token_company, create_category_dish):
        create_category_dish()
        token_company, company = get_token_company
        url = reverse('DINNER:list_all_category')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        user_data[0]['name'] = 'Первые блюда'

    def test_get_dish(self, api_client, get_token_company, create_dish):
        create_dish()
        token_company, company = get_token_company
        url = reverse('DINNER:list_all_dish')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        user_data[0]['name'] = 'Томатный суп'

    def test_get_list_complex_dinner(self, api_client, get_token_company, create_complex_dish):
        create_complex_dish()
        token_company, company = get_token_company
        url = reverse('DINNER:list_all_complex_dinner')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        response = api_client.get(url)
        user_data = json.loads(response.content)

        assert response.status_code == 200
        user_data[0]['name'] = 'Комплексный обед №2'

    def test_change_dish(self, api_client, get_token_company, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:change_dish', kwargs={"dish_id": create_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "name": "Пельмеши",
            "added_dish": [
                {
                    "id": create_dish().id
                }
            ]
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)
        assert response.status_code == 200
        user_data['name'] = "Пельмеши"

    def test_change_category_dish(self, api_client, get_token_company, create_category_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:change_dish_category', kwargs={"dish_category_id": create_category_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "name": "Последние блюда"
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)
        assert response.status_code == 200
        user_data['name'] = "Последние блюда"

    def test_change_complex_dish(self, api_client, get_token_company, create_complex_dish, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:change_complex_dinner', kwargs={"complex_id": create_complex_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "name": "Комплексный обед №3",
            "dishes": [
                {
                    "id": create_dish().id,
                    "is_remove": True
                }
            ]
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        user_data = json.loads(response.content)
        assert response.status_code == 200
        user_data['name'] = "Комплексный обед №3"

    def test_change_day_menu(self, api_client, get_token_company, create_menu, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:change_menu', kwargs={"menu_id": create_menu().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)

        data = {
            "dish": [
                {
                    "id": create_dish().id,
                    "is_remove": True
                }
            ],
            "available_order_date": "2020-05-03"
        }

        response = api_client.put(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200

    def test_delete_dish(self, api_client, get_token_company, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:delete_dish', kwargs={"dish_id": create_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_delete_category_dish(self, api_client, get_token_company, create_category_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:delete_dish_category', kwargs={"dish_category_id": create_category_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_delete_complex_dish(self, api_client, get_token_company, create_complex_dish, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:delete_complex_dinner', kwargs={"complex_id": create_complex_dish().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)
        response = api_client.delete(url)

        assert response.status_code == 204

    def test_delete_day_menu(self, api_client, get_token_company, create_menu, create_dish):
        token_company, company = get_token_company
        url = reverse('DINNER:delete_menu', kwargs={"menu_id": create_menu().id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_company.key)
        response = api_client.delete(url)

        assert response.status_code == 204
