from rest_framework import serializers

from apps.dinner.models import Menu, Dish, MenuGroup


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id', 'name', 'cost', 'weight', 'composition', 'menu_group', 'added_dish')


class DishGroupSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = MenuGroup
        fields = ['id', 'name', 'dishes']


class MenuSerializer(serializers.ModelSerializer):
    dish = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['id', 'dish', 'available_order_date', 'close_order_time']
