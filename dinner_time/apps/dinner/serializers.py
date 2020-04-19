from rest_framework import serializers

from apps.dinner.models import *
from apps.dinner.utils import create_additional_dish


class AddedDishSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='from_dish.name')

    class Meta:
        model = AddedDish
        fields = ('id', 'name', 'for_complex', 'сomplex_dinner')


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for dish with update method
    """

    id = serializers.IntegerField(read_only=False, required=False)
    added_dish = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ('id', 'name', 'cost', 'weight', 'composition', 'menu_group', 'added_dish')

    def get_added_dish(self, obj):
        is_complex = self.context.get("for_complex", False)
        qs = AddedDish.objects.filter(to_dish=obj, for_complex=is_complex)
        return [AddedDishSerializer(m).data for m in qs]

    def create(self, validated_data):
        validated_data.pop('added_dish', None)
        create_dish = Dish.objects.create(**validated_data)

        if self.initial_data.get("added_dish"):
            for dish in self.initial_data.get("added_dish"):
                dish_id = dish.get("id")
                AddedDish.objects.get_or_create(to_dish=create_dish, from_dish=Dish.objects.get(pk=dish_id))

        return create_dish

    def update(self, instance, validated_data):
        dishes = self.initial_data.get("added_dish", [])

        for dish in dishes:
            dish_id = dish.get("id")

            AddedDish.objects.get_or_create(to_dish=instance, from_dish=Dish.objects.get(pk=dish_id))

        instance.menu_group = validated_data.pop('menu_group', None)
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class ComplexDinnerSerializer(serializers.ModelSerializer):
    """
    Serializer for complex dinner with create and update method
    """

    dishes = DishSerializer(many=True, required=False)

    class Meta:
        model = ComplexDinner
        fields = ['id', 'name', 'dishes']

    def create(self, validated_data):
        validated_data.pop("dishes", None)
        dishes = self.initial_data.get("dishes", [])

        complex_dinner = ComplexDinner.objects.create(**validated_data)
        create_additional_dish(dishes, complex_dinner)
        return complex_dinner

    def update(self, instance, validated_data):
        validated_data.pop("dishes", None)
        dishes = self.initial_data.get("dishes")

        create_additional_dish(dishes, instance)

        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


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
