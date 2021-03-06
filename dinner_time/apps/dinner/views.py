from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import pagination
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.dinner.serializers import *
from .data_for_swagger import *


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
    permission_classes = [IsAuthenticated]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_object(self):
        return get_object_or_404(Dish, id=self.kwargs.get("dish_id"))


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Получение категорий меню вместе с блюдами.',
    operation_description='''
Метод позволяет:
1) получить все категории меню вместе с блюдами.
2) при передаче "category_id", получаем только блюда в выбранной категории.
''',

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
    permission_classes = [IsAuthenticated]
    serializer_class = DishCategorySerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return CategoryDish.objects.filter(id=category_id)

        return CategoryDish.objects.all()

    def get_object(self):
        return get_object_or_404(CategoryDish, id=self.kwargs.get("dish_category_id"))


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Получение информации по комлпексным(-ому) обедам(-у).',
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
    permission_classes = [IsAuthenticated]
    queryset = ComplexDinner.objects.all()
    serializer_class = ComplexDinnerSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_object(self):
        return get_object_or_404(ComplexDinner, id=self.kwargs.get("complex_id"))

    def get_serializer_context(self):
        return {'for_complex': True}


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Получение информации по дневному меню.',
    responses={
        '200': openapi.Response('Успешно', MenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление данных дневного меню.',
    operation_description='''
Метод позволяет:
1) добавить блюда в меню путем добавления "id" блюда в dish.
2) удалять блюда путем добавления "id" блюда в dish и постановки флага is_remove.
3) добавить комплексный обед в меню путем добавления "id" комплексного обеда в complex_dinner.
4) удалять комплексный обед путем добавления "id" комплексного обеда в complex_dinner и постановки флага is_remove.
5) менять дату показа этого меню.
''',
    request_body=request_for_create_menu,
    responses={
        '200': openapi.Response('Успешно', MenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание меню.',
    operation_description='''
Метод позволяет:
1) собрать меню из блюд путем добавления "id" блюда в dish.
2) собрать комплексный обед путем добавления "id" комплексного обеда в complex_dinner.
3) установить дату показа этого меню.
4) number_day - является номером дня недели, где 0 - это воскресенье (нужно для темлейтов)
''',
    request_body=request_for_create_menu,
    responses={
        '201': openapi.Response('Создано', MenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class MenuViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DayMenu.objects.all()
    serializer_class = MenuSerializer

    def get_object(self):
        return get_object_or_404(DayMenu, id=self.kwargs.get("menu_id"))


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Просмотр темплейта.',
    responses={
        '200': openapi.Response('Успешно', TemplateSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление темплейта.',
    operation_description='''
Метод позволяет:
1) изменить название шаблона.
2) изменить номер недели для показа (1-4).

ps: если надо менять что то по блюдам, то все запросы в раздел блюда
''',
    request_body=request_for_template,
    responses={
        '200': openapi.Response('Успешно', TemplateSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Удаление темплейта.',
    responses={
        '204': 'Удалено',
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание шаблона.',
    operation_description='''
Как работает?
1) дать название этому шаблону.
2) выставить номер недели, на которой будет показываться шаблон.
3) добавить "id" недельного меню.
''',
    request_body=request_for_template,
    responses={
        '201': openapi.Response('Создано', TemplateSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class TemplateViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def get_object(self):
        return get_object_or_404(Template, id=self.kwargs.get("pk"))


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Просмотр недельного меню.',
    responses={
        '200': openapi.Response('Успешно', WeekMenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Обновление недельного меню.',
    operation_description='''
Метод позволяет:
1) добавить в недельное меню еще один день, путем передачи "id" дневного меню.
2) удалить из недельного меню дневное меню, путем передачи "id" дневного меню с флагом "remove": true.
''',
    request_body=request_for_remove_day_menu_from_week_menu,
    responses={
        '200': openapi.Response('Успешно', WeekMenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Удаление недельного меню.',
    responses={
        '204': 'Удалено',
        '400': 'Неверный формат запроса'
    }
)
                  )
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Создание недельного меню.',
    operation_description='''
Передаем в "id" значение из DayMenu.
''',
    request_body=request_for_week_menu,
    responses={
        '201': openapi.Response('Создано', WeekMenuSerializer),
        '400': 'Неверный формат запроса'
    }
)
                  )
class WeekMenuViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = WeekMenu.objects.all()
    serializer_class = WeekMenuSerializer

    def get_object(self):
        return get_object_or_404(WeekMenu, id=self.kwargs.get("pk"))
