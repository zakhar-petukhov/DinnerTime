from rest_framework import serializers
from apps.dinner.models import Menu, Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name', 'cost', 'weight', 'composition', 'menu_group', 'added_dish')


class MenuSerializer(serializers.ModelSerializer):
    dish = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['dish', 'available_order_date', 'close_order_time']
