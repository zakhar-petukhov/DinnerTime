from rest_framework import serializers

from apps.dinner.models import Menu, Dish, MenuGroup


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class DishSerializer(serializers.ModelSerializer):
    additional_dish = RecursiveField(many=True, required=False)

    class Meta:
        model = Dish
        fields = ('id', 'name', 'cost', 'weight', 'composition', 'menu_group', 'added_dish', 'additional_dish')


class DishGroupSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, required=False)

    class Meta:
        model = MenuGroup
        fields = ['id', 'name', 'dishes']


class MenuSerializer(serializers.ModelSerializer):
    dish = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['id', 'dish', 'available_order_date', 'close_order_time']
