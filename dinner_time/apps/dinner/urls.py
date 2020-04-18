from django.urls import path

from .views import *

app_name = "DINNER"

urlpatterns = [
    path('create_dish/', DishViewSet.as_view({'post': 'create'}), name='create_dish'),
    path('create_dish_group/', DishGroupViewSet.as_view({'post': 'create'}), name='create_dish_group'),
    path('create_complex_dinner/', ComplexDinnerViewSet.as_view({'post': 'create'}), name='create_complex_dinner'),

    path('list_all_dish/', DishViewSet.as_view({'get': 'list'}), name='list_all_dish'),
    path('list_all_group/', DishGroupViewSet.as_view({'get': 'list'}), name='list_all_group'),
    path('list_complex_dinner/', ComplexDinnerViewSet.as_view({'get': 'list'}), name='list_all_complex_dinner'),

    path('change_dish/<dish_id>', DishViewSet.as_view({'put': 'update'}), name='change_dish'),
    path('change_dish_group/<dish_group_id>', DishGroupViewSet.as_view({'put': 'update'}), name='change_dish_group'),
    path('change_complex_dinner/<complex_id>/',
         ComplexDinnerViewSet.as_view({'put': 'update'}, name='change_complex_dinner'),
         name='change_complex_dinner'),

]
