from django.db.models import *


class CompanyOrder(Model):
    dinner = ForeignKey('dinner.DinnerOrder', on_delete=PROTECT, related_name='dinner_dish', verbose_name='Меню',
                        blank=True, null=True)
    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, verbose_name='Создано')

    class Meta:
        verbose_name = "Одобренное меню"
        verbose_name_plural = "Одобренное меню"


class DinnerOrder(Model):
    dish = ForeignKey('dinner.Dish', on_delete=PROTECT, related_name='dinner_dish', verbose_name='Блюдо',
                      blank=True, null=True)
    date_action_begin = DateTimeField(null=True, blank=True)
    status = CharField(max_length=11, choices=[
        ('processing', 'В обработке'),
        ('accept', 'Принято')], verbose_name='Статус', blank=True, default='processing')
    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, verbose_name='Создано')
    update_date = DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')

    @property
    def get_full_cost(self):
        full_cost = 0
        all_dinner = DinnerOrder.objects.all()
        for obj in all_dinner:
            full_cost += obj.dish.cost

        return full_cost

    class Meta:
        verbose_name = "Неодобренное меню"
        verbose_name_plural = "Неодобренное меню"


class MenuGroup(Model):
    name = CharField(max_length=40, blank=True, null=True, verbose_name='Название группы')

    def __str__(self):
        return self.name


class Dish(Model):
    name = CharField(max_length=40, blank=True, null=True, verbose_name='Название блюда')
    cost = FloatField(unique=False, verbose_name='Цена')
    weight = FloatField(unique=False, verbose_name='Вес')
    composition = CharField(max_length=120, blank=True, null=True, verbose_name='Состав')
    menu_group = ForeignKey(MenuGroup, on_delete=PROTECT, related_name='menu_group', verbose_name='Группа меню',
                            blank=True, null=True)
    added_dish = ForeignKey('self', on_delete=CASCADE, related_name='additional_menu',
                            verbose_name='Дополнительное блюдо', blank=True, null=True)

    @classmethod
    def search(cls, name: str,
               queryset=None):
        """
        Метод поиска по объектам класса Dish

        @param name: (str) Искомое значение
                Строка в любом регистре
        @param queryset: (QuerySet) Использовать готовый queryser для поиска в диапазоне переданной выборки

        @return: QuerySet
        """

        name = str(name).title()

        """
            Если не передан QuerySet то поиск производится по всем блюдам
        """
        if not queryset:
            queryset = cls.objects.all()

        """
            Поиск будет производится только среди моделей определенного блюда
        """
        if name:
            queryset = queryset.filter(name=name)

        return queryset

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюдо"