from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.dinner.serializers import *


# @method_decorator(name='update', decorator=swagger_auto_schema(
#     operation_summary='Обновление данных блюда',
#     operation_description='''
# ''',
#     request_body=DishSerializer,
#     responses={
#         '200': openapi.Response('Успешно', DishSerializer),
#         '400': 'Неверный формат запроса'
#     }
# )
#                   )
# @method_decorator(name='create', decorator=swagger_auto_schema(
#     operation_summary='Создание блюда',
#     operation_description='''
# При создании блюда указывается все важные параметры:
# 1) Название
# 2) Стоимость
# 3) Вес
# 4) Состав
# Также можно сразу прикрепить к определенной категорий блюд
# ''',
#     request_body=DishSerializer,
#     responses={
#         '201': openapi.Response('Создано', DishSerializer),
#         '400': 'Неверный формат запроса'
#     }
# )
#                   )
# @method_decorator(name='list', decorator=swagger_auto_schema(
#     operation_summary='Получение всех блюд',
#     request_body=DishSerializer,
#     responses={
#         '200': openapi.Response('Успешно', DishSerializer),
#         '400': 'Неверный формат запроса'
#     }
# )
#                   )
class DishViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Dish.objects.filter(for_complex=False)
    serializer_class = DishSerializer

    def get_object(self):
        return get_object_or_404(Dish, id=self.kwargs.get("dish_id"))


class DishGroupViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MenuGroup.objects.filter(dishes__for_complex=False)
    serializer_class = DishGroupSerializer

    def get_object(self):
        return get_object_or_404(MenuGroup, id=self.kwargs.get("dish_group_id"))


class ComplexDinnerViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ComplexDinner.objects.all()
    serializer_class = ComplexDinnerSerializer

    def get_object(self):
        return get_object_or_404(ComplexDinner, id=self.kwargs.get("complex_id"))
