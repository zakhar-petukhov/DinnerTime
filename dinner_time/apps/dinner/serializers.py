from django.db import transaction
from rest_framework import serializers

from apps.dinner.models import *


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class DishSerializer(serializers.ModelSerializer):
    added_dish = RecursiveField(many=True, required=False)

    class Meta:
        model = Dish
        fields = ('id', 'name', 'cost', 'weight', 'composition', 'menu_group', 'added_dish', 'for_complex')

    @transaction.atomic
    def update(self, instance, validated_data):
        dishes = self.initial_data.get("added_dish")

        for dish in dishes:
            id = dish.get("id")
            instance.pk = None
            instance.save()
            # instance.added_dish.create(Dish.objects.get(pk=id))

        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class ComplexDinnerSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, required=False)

    @transaction.atomic
    def update(self, instance, validated_data):
        dishes = self.initial_data.get("dishes")

        for dish in dishes:
            id = dish.get("id")
            copy_dish = Dish.objects.filter(pk=id).first()
            copy_dish.pk = None
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
    dishes = DishSerializer(many=True, required=False)

    class Meta:
        model = MenuGroup
        fields = ['id', 'name', 'dishes']


class MenuSerializer(serializers.ModelSerializer):
    dish = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['id', 'dish', 'available_order_date', 'close_order_time']
