from django.urls import path

from .views import *

app_name = "DINNER"

urlpatterns = [
    path('create_dish/', DishViewSet.as_view({'post': 'create'}), name='create_dish'),
    path('create_dish_category/', DishCategoryViewSet.as_view({'post': 'create'}), name='create_dish_category'),
    path('create_complex_dinner/', ComplexDinnerViewSet.as_view({'post': 'create'}), name='create_complex_dinner'),
    path('create_menu/', MenuViewSet.as_view({'post': 'create'}), name='create_menu'),

    path('list_menu/', MenuViewSet.as_view({'get': 'list'}), name='list_all_menu'),
    path('list_all_dish/', DishViewSet.as_view({'get': 'list'}), name='list_all_dish'),
    path('list_all_category/', DishCategoryViewSet.as_view({'get': 'list'}), name='list_all_category'),
    path('list_complex_dinner/', ComplexDinnerViewSet.as_view({'get': 'list'}), name='list_all_complex_dinner'),

    path('detail_complex_dinner/<complex_id>/', ComplexDinnerViewSet.as_view({'get': 'list'}),
         name='detail_complex_dinner'),

    path('change_menu/<menu_id>/', MenuViewSet.as_view({'put': 'update'}), name='change_menu'),
    path('change_dish/<dish_id>/', DishViewSet.as_view({'put': 'update'}), name='change_dish'),
    path('change_dish_category/<dish_category_id>/', DishCategoryViewSet.as_view({'put': 'update'}),
         name='change_dish_category'),
    path('change_complex_dinner/<complex_id>/',
         ComplexDinnerViewSet.as_view({'put': 'update'}, name='change_complex_dinner'),
         name='change_complex_dinner'),

    path('delete_menu/<menu_id>/', MenuViewSet.as_view({'delete': 'destroy'}), name='delete_menu'),
    path('delete_dish/<dish_id>', DishViewSet.as_view({'delete': 'destroy'}), name='delete_dish'),
    path('delete_dish_category/<dish_category_id>', DishCategoryViewSet.as_view({'delete': 'destroy'}),
         name='delete_dish_category'),
    path('delete_complex_dinner/<complex_id>/',
         ComplexDinnerViewSet.as_view({'delete': 'destroy'}, name='delete_complex_dinner'),
         name='delete_complex_dinner'),

]
