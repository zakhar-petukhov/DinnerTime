import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.company.models import Company, Department
from apps.dinner.models import CategoryDish, Dish, ComplexDinner, DayMenu
from apps.users.models import User
from apps.utils.models import Settings


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_company(db, django_user_model):
    def make_company():
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
            "email": "test_company@mail.ru",
            "username": "test_company",
            "password": 'test_company',
        }

        company_data = data['company_data']
        company, _ = Company.objects.get_or_create(**company_data)
        data['company_data'] = company
        manager_with_company, _ = User.objects.get_or_create(**data)
        return manager_with_company

    return make_company


@pytest.fixture
def create_department(db, django_user_model, get_token_company):
    def make_department():
        token, company = get_token_company
        data = {
            "name": "Любители вкусняшек",
            "company": company.company_data
        }

        return Department.objects.create(**data)

    return make_department


@pytest.fixture
def create_category_dish(django_user_model, get_token_company):
    def make_category_dish():
        data = {
            "name": "Первые блюда"
        }

        return CategoryDish.objects.create(**data)

    return make_category_dish


@pytest.fixture
def create_dish(django_user_model, get_token_company, create_category_dish):
    def make_dish():
        data = {
            "name": "Томатный суп",
            "cost": 90,
            "weight": 120,
            "composition": "Томат, горох",
            "category_dish": create_category_dish()
        }

        return Dish.objects.create(**data)

    return make_dish


@pytest.fixture
def create_complex_dish(django_user_model, get_token_company, create_dish):
    def make_complex_dish():
        data = {
            "name": "Комплексный обед №2",
        }

        Settings.objects.create()  # create the settings to take effect
        complex_dinner = ComplexDinner.objects.create(**data)
        complex_dinner.dishes.add(create_dish())

        return complex_dinner

    return make_complex_dish


@pytest.fixture
def create_menu(django_user_model, get_token_company, create_dish, create_complex_dish):
    def make_menu():
        day_menu = DayMenu.objects.create()
        day_menu.complex_dinner.add(create_complex_dish())
        day_menu.dish.add(create_dish())

        return day_menu

    return make_menu


@pytest.fixture
def get_token_user(db, create_user, create_company):
    user = create_user(phone='89313147222', first_name='Тест', last_name="Тестовов",
                       email='test@protonmail.com', username='test', password='test', is_superuser=True,
                       is_staff=True)
    token, _ = Token.objects.get_or_create(user=user)
    return token, user


@pytest.fixture
def get_token_company(db, create_company):
    company = create_company()
    token, _ = Token.objects.get_or_create(user=company)
    return token, company
