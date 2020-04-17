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

    added_dish = RecursiveField(many=True, required=False)

    class Meta:
        model = Dish
        fields = ('id', 'name', 'cost', 'weight', 'composition', 'menu_group', 'added_dish', 'for_complex')

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
        choice_validated_data = validated_data.pop('dishes')
        complex_dinner = ComplexDinner.objects.create(**validated_data)
        choice_set_serializer = self.fields['dishes']

        for dish in choice_validated_data:
            create_dish = Dish.objects.create(**dish, for_complex=True)
            complex_dinner.dishes.add(create_dish)
            choice_set_serializer.create(choice_validated_data)

        return complex_dinner

    def update(self, instance, validated_data):
        dishes = self.initial_data.get("dishes")

        for dish in dishes:
            id = dish.get("id")
            copy_dish = Dish.objects.filter(pk=id).first()
            copy_dish.pk = None  # Create duplicate dish and add flag for_complex
            copy_dish.for_complex = True
            copy_dish.save()
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
