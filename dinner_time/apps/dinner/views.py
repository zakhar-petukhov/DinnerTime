from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.dinner.serializers import *
from .data_for_swagger import request_for_dish, request_for_complex_dinner, request_for_create_category_dish, \
    request_for_update_category_dish


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Получение всех блюд.',
    operation_description='Получение всех блюд вместе с гарнирами (если присутствует).',
    responses={
        '200': openapi.Response('Успешно', DishSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление данных блюда.',
    operation_description='''
Метод позволяет:
1) добавлять блюда в категорию, путем передачи "id" категории в "category_dish".
2) изменять основную информацию о блюде.
2) добавлять гарнир, путем передачи "id" другого блюда в список "added_dish".
''',
    request_body=request_for_dish,
    responses={
        '200': openapi.Response('Успешно', DishSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание блюда.',
    operation_description='''
Метод позволяет:
1) создать просто блюдо без гарниров
2) добавить сразу гарнир, путем передачи "id" другого блюда в список "added_dish".''',
    request_body=request_for_dish,
    responses={
        '201': openapi.Response('Создано', DishSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class DishViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def get_object(self):
        return get_object_or_404(Dish, id=self.kwargs.get("dish_id"))


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Получение всех категорий меню вместе с блюдами.',
    responses={
        '200': openapi.Response('Успешно', DishCategorySerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление названия категории.',
    request_body=request_for_update_category_dish,
    responses={
        '200': openapi.Response('Успешно', DishCategorySerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание категории.',
    request_body=request_for_create_category_dish,
    responses={
        '201': openapi.Response('Создано', DishCategorySerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class DishCategoryViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CategoryDish.objects.all()
    serializer_class = DishCategorySerializer

    def get_object(self):
        return get_object_or_404(CategoryDish, id=self.kwargs.get("dish_category_id"))


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Получение всех комплексных обедов.',
    responses={
        '200': openapi.Response('Успешно', ComplexDinnerSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление данных комплексного обеда.',
    operation_description='''
Метод позволяет:
1) добавлять блюда в комплексный обед, путем добавления "id" главного блюда, также можно передать его гарнир, \
путем добавления "id" гарнира в список added_dish.
2) изменять информацию самого обеда.
''',
    request_body=request_for_complex_dinner,
    responses={
        '200': openapi.Response('Успешно', ComplexDinnerSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание комплексного обеда.',
    operation_description='''
Метод позволяет:
1) создать просто название комплексного обеда, без блюд.
2) прикреплять блюда сразу при создании комплексного обеда путем добавления "id" главного блюда, также можно сразу \
передать его гарнир, путем добавления "id" гарнира в список added_dish.
''',
    request_body=request_for_complex_dinner,
    responses={
        '201': openapi.Response('Создано', ComplexDinnerSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class ComplexDinnerViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ComplexDinner.objects.all()
    serializer_class = ComplexDinnerSerializer

    def get_object(self):
        return get_object_or_404(ComplexDinner, id=self.kwargs.get("complex_id"))

    def get_serializer_context(self):
        return {'for_complex': True}