from django.db import transaction
from rest_framework import serializers

from apps.dinner.models import *


class RecursiveField(serializers.Serializer):
    """
    Recursive serializer for get all added dish
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for dish with update method
    """
    id = serializers.IntegerField(read_only=False, required=False)
    added_dish = RecursiveField(many=True, required=False)

    class Meta:
        model = Dish
        fields = ('id', 'name', 'cost', 'weight', 'composition', 'menu_group', 'added_dish')

    def create(self, validated_data):
        validated_data.pop('added_dish')
        create_dish = Dish.objects.create(**validated_data)

        for dish in self.initial_data.get("added_dish"):
            dish_id = dish.get("id")
            create_dish.added_dish.add(dish_id)

        return create_dish

    @transaction.atomic
    def update(self, instance, validated_data):
        dishes = self.initial_data.get("added_dish")

        for dish in dishes:
            id = dish.get("id")
            instance.added_dish.add(Dish.objects.get(pk=id))

        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class ComplexDinnerSerializer(serializers.ModelSerializer):
    """
    Serializer for complex dinner with create and update method
    """

    dishes = DishSerializer(many=True, required=False)

    def create(self, validated_data):
        dishes = validated_data.pop('dishes')
        complex_dinner = ComplexDinner.objects.create(**validated_data)

        for dish in dishes:
            dish_id = dish.get("id")
            copy_dish = Dish.objects.filter(pk=dish_id).first()
            complex_dinner.dishes.add(copy_dish)

        return complex_dinner

    def update(self, instance, validated_data):
        dishes = self.initial_data.get("dishes")

        for dish in dishes:
            dish_id = dish.get("id")
            copy_dish = Dish.objects.filter(pk=dish_id).first()
            instance.dishes.add(copy_dish)

        instance.__dict__.update(**validated_data)
        instance.save()
        return instance

    class Meta:
        model = ComplexDinner
        fields = ['id', 'name', 'dishes']


class DishGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for category dish
    """

    dishes = DishSerializer(many=True, required=False)

    class Meta:
        model = MenuGroup
        fields = ['id', 'name', 'dishes']


class MenuSerializer(serializers.ModelSerializer):
    dish = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['id', 'dish', 'available_order_date', 'close_order_time']
