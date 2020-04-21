from apps.dinner.models import Dish, AddedDish


def get_additional_dish_for_complex(initial_data, сomplex_dinner):
    """
    In this function:
    1) we can add dish with side dish or not in list dishes
    2) can remove dish and his side dish
    3) use for complex dinner
    """

    for dish in initial_data:
        main_dish_id = dish.get("id")
        added_dish = dish.get("added_dish", [])
        is_remove = dish.get("is_remove", False)

        main_dish = Dish.objects.get(pk=main_dish_id)

        if is_remove:
            return сomplex_dinner.dishes.remove(main_dish)

        get_additional_dish(initial_data=added_dish, main_dish=main_dish, for_complex=True,
                            сomplex_dinner=сomplex_dinner)


def get_additional_dish(initial_data, main_dish, for_complex=False, сomplex_dinner=None):
    """
    In this function:
    1) we can add side dish into dish
    2) can remove side dish
    3) use for additional dish
    """

    for second_course in initial_data:
        second_dish_id = second_course.get("id")
        second_dish_is_remove = second_course.get("is_remove", False)

        added_dish, is_create = AddedDish.objects.get_or_create(to_dish=main_dish,
                                                                from_dish=Dish.objects.get(pk=second_dish_id),
                                                                for_complex=for_complex,
                                                                сomplex_dinner=сomplex_dinner)
        if second_dish_is_remove:
            return added_dish.delete()

        main_dish = added_dish.to_dish

    if сomplex_dinner:
        return сomplex_dinner.dishes.add(main_dish)
