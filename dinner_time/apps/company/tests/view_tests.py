import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestCompanyView:
    def test_company_create(self, api_client, get_or_create_token):
        url = reverse('COMPANY:create_company')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_or_create_token.key)

        data = {
            "company_data": {
                "company_name": "ООО Тест",
                "full_address": "ул. Пушкина, дом Колотушкина",
                "registration_date": "2020-04-25"
            },
            "first_name": "Тест",
            "last_name": "Тестов",
            "middle_name": "Тестович",
            "phone": "89313123442",
            "email": "test_company@mail.ru"
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        company_data = json.loads(response.content)

        assert response.status_code == 201
        assert company_data['company_data']['company_name'] == "ООО Тест"
        assert company_data['first_name'] == "Тест"

    def test_list_all_company(self, api_client, get_or_create_token, create_company):
        create_company()
        url = reverse('COMPANY:all_companies')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_or_create_token.key)

        response = api_client.get(path=url)
        company_data = json.loads(response.content)

        assert response.status_code == 200
        assert company_data[0]['company_data']['company_name'] == "ООО Тест"
        assert company_data[0]['first_name'] == "Тест"

    def test_list_detail_company(self, api_client, get_or_create_token, create_company):
        company = create_company()
        url = reverse('COMPANY:detail_company', kwargs={'company_id': company.id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_or_create_token.key)

        response = api_client.get(path=url)
        company_data = json.loads(response.content)

        assert response.status_code == 200
        assert company_data[0]['company_data']['company_name'] == "ООО Тест"
        assert company_data[0]['first_name'] == "Тест"

    def test_change_detail_company(self, api_client, get_or_create_token, create_company):
        company = create_company()
        url = reverse('COMPANY:change_detail_company', kwargs={'company_id': company.id})
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_or_create_token.key)

        data = {
            "company_data": {
                "company_name": "ООО Тестик",
            },
            "is_blocked": True,
            "is_active": False
        }

        response = api_client.put(path=url, data=data)
        company_data = json.loads(response.content)

        assert response.status_code == 200
        assert company_data['company_data']['company_name'] == "ООО Тестик"
        assert company_data['is_blocked'] is True


@pytest.mark.django_db
class TestDepartmentView:
    def test_department_create(self, api_client, get_or_create_token_company):
        url = reverse('COMPANY:department-create-department')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_or_create_token_company.key)

        data = {
            "name": "IT отдел"
        }

        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        department_data = json.loads(response.content)

        assert response.status_code == 201
        assert department_data['name'] == "IT отдел"

    def test_list_all_department(self, api_client, get_or_create_token_company):
        url = reverse('COMPANY:department-list')
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_or_create_token_company.key)
        response = api_client.get(path=url)

        assert response.status_code == 200

    # def test_add_employee_into_department(self, api_client, get_or_create_token_company):
    #     url = reverse('COMPANY:department-add-user')
    #     api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_or_create_token_company.key)
