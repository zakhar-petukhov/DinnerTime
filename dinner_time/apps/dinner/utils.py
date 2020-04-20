from apps.dinner.models import Dish, AddedDish


def create_additional_dish_for_complex(initial_data, сomplex_dinner):
    for dish in initial_data:
        main_dish_id = dish.get("id")
        added_dish = dish.get("added_dish", [])

        main_dish = Dish.objects.get(pk=main_dish_id)

        for second_course in added_dish:
            second_dish_id = second_course.get("id")

            main_dish, is_create = AddedDish.objects.get_or_create(to_dish=main_dish,
                                                                   from_dish=Dish.objects.get(pk=second_dish_id),
                                                                   for_complex=True,
                                                                   сomplex_dinner=сomplex_dinner)
            main_dish = main_dish.to_dish

        сomplex_dinner.dishes.add(main_dish)


def create_additional_dish(initial_data, main_dish):
    for dish in initial_data:
        dish_id = dish.get("id")
        AddedDish.objects.get_or_create(to_dish=main_dish, from_dish=Dish.objects.get(pk=dish_id))
