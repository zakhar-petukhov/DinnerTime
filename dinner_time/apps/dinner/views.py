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
    operation_description='Получение всех блюд вместе с гарнирами (если это предусмотрено).',
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
1) добавлять блюда в категорию, путем передачи id категории в menu_group.
2) изменять основную информацию о блюде.
2) добавлять к блюду гарниры, путем передачи id блюда в added_dish и проставления флага принадлежности к  \
комплексному обеду.
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
2) добавить сразу гарнир, путем передачи в added_dish id другого блюда и установки флага пренадлежности к \
комплексному обеду.''',
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
        '200': openapi.Response('Успешно', DishGroupSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление названия категории.',
    request_body=request_for_update_category_dish,
    responses={
        '200': openapi.Response('Успешно', DishGroupSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание категории.',
    request_body=request_for_create_category_dish,
    responses={
        '201': openapi.Response('Создано', DishGroupSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class DishGroupViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MenuGroup.objects.all()
    serializer_class = DishGroupSerializer

    def get_object(self):
        return get_object_or_404(MenuGroup, id=self.kwargs.get("dish_group_id"))


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
1) добавлять блюда в комплексный обед, путем вставки id блюда в список dishes.
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
Можно создать комплексный обед путем заполнения только его названия, а блюда добавлять в методе PUT, либо \
можно сразу добавлять блюда внутри списка dishes.
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
