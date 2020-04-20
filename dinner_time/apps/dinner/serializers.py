from rest_framework import serializers

from apps.dinner.models import *
from apps.dinner.utils import create_additional_dish, create_additional_dish_for_complex


class AddedDishSerializer(serializers.ModelSerializer):
    """
    Serializer for add dish to dish
    """

    name = serializers.CharField(source='from_dish.name')
    cost = serializers.FloatField(source='from_dish.cost')
    weight = serializers.FloatField(source='from_dish.weight')
    composition = serializers.CharField(source='from_dish.composition')
    category_dish = serializers.IntegerField(source='from_dish.category_dish.id')

    class Meta:
        model = AddedDish
        fields = ('id', 'name', 'cost', 'weight', 'composition', 'category_dish', 'for_complex', 'сomplex_dinner')


class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for dish with create and update method
    """

    id = serializers.IntegerField(read_only=False, required=False)
    added_dish = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ('id', 'name', 'cost', 'weight', 'composition', 'category_dish', 'added_dish')

    def get_added_dish(self, obj):
        is_complex = self.context.get("for_complex", False)
        complex_id = self.context.get("complex_id", None)

        qs = AddedDish.objects.filter(to_dish=obj, for_complex=is_complex, сomplex_dinner=complex_id)
        return [AddedDishSerializer(m).data for m in qs]

    def create(self, validated_data):
        validated_data.pop('added_dish', None)
        create_dish = Dish.objects.create(**validated_data)
        dishes = self.initial_data.get("added_dish", [])
        create_additional_dish(dishes, create_dish)
        return create_dish

    def update(self, instance, validated_data):
        dishes = self.initial_data.get("added_dish", [])
        create_additional_dish(dishes, instance)
        instance.category_dish = validated_data.pop('category_dish', instance.category_dish)
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class ComplexDinnerSerializer(serializers.ModelSerializer):
    """
    Serializer for complex dinner with create and update method
    """

    dishes = serializers.SerializerMethodField()

    class Meta:
        model = ComplexDinner
        fields = ['id', 'name', 'dishes']

    def get_dishes(self, obj):
        self.context["complex_id"] = obj.id
        serializer = DishSerializer(many=True, required=False, context=self.context, data=obj.dishes)
        serializer.is_valid()
        return serializer.data

    def create(self, validated_data):
        validated_data.pop("dishes", None)
        complex_dinner = ComplexDinner.objects.create(**validated_data)
        create_additional_dish_for_complex(self.initial_data.get("dishes", []), complex_dinner)
        return complex_dinner

    def update(self, instance, validated_data):
        validated_data.pop("dishes", None)
        create_additional_dish_for_complex(self.initial_data.get("dishes", []), instance)
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class DishCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for category dish
    """

    dishes = DishSerializer(many=True, required=False)

    class Meta:
        model = CategoryDish
        fields = ['id', 'name', 'dishes']


class MenuSerializer(serializers.ModelSerializer):
    dish = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['id', 'dish', 'available_order_date', 'close_order_time']
