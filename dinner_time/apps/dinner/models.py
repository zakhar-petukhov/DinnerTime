import datetime

from django.db.models import *

from apps.users.models import User
from apps.utils.models import Settings


class CompanyOrder(Model):
    company = ForeignKey(User, on_delete=PROTECT, related_name='dinners_orders', blank=True, null=True,
                         verbose_name='Компания')
    dinners = ManyToManyField('dinner.Dinner', related_name='in_orders', blank=True, verbose_name='Заказанные обеды')

    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, verbose_name='Создано')

    class Meta:
        verbose_name = "Одобренное меню"
        verbose_name_plural = "Одобренное меню"


class Dinner(Model):
    IN_PROCESSING = 0
    ACCEPTED = 1
    CANCELED = 2
    CONFIRMED = 3
    STATUSES = [
        (IN_PROCESSING, 'В обработке'),
        (ACCEPTED, 'Принят'),
        (CANCELED, 'Отменен'),
        (CONFIRMED, 'Подтвержден'),
    ]

    dishes = ManyToManyField('dinner.Dish', related_name='dinner_dishes', verbose_name='Блюдо', blank=True)

    date_action_begin = DateField(null=True, blank=True, verbose_name='Заказ на дату')
    status = SmallIntegerField(choices=STATUSES, blank=True, default=IN_PROCESSING, verbose_name='Статус')

    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, verbose_name='Создано')
    update_date = DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')

    is_complex = BooleanField(default=False, verbose_name='Комплексный обед')
    complex_cost = FloatField(blank=True, null=True, verbose_name='Цена за комплексный обед')
    available_complex_order_date = DateField(unique=True, null=True, blank=True,
                                             verbose_name='Комлпексный обед доступен на дату')

    @property
    def full_cost(self):
        cost = 0 or self.complex_cost
        if not cost:
            all_dinner = self.dishes.all()
            for obj in all_dinner:
                cost += obj.dish.cost

        return cost

    @property
    def status_name(self):
        if self.status:
            return self.STATUSES[self.status][1]
        return 'Без статуса'

    class Meta:
        verbose_name = "Обед"
        verbose_name_plural = "Обед"


class CategoryDish(Model):
    name = CharField(max_length=40, blank=True, null=True, verbose_name='Название группы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория блюд"
        verbose_name_plural = "Категория блюд"


class ComplexDinner(Model):
    name = CharField(max_length=40, blank=True, null=True, verbose_name='Название комплексного обеда')
    dishes = ManyToManyField('dinner.Dish', related_name='complex_dishes', verbose_name='Блюда', blank=True)

    class Meta:
        verbose_name = "Комплексный обед"
        verbose_name_plural = "Комплексный обед"


class Dish(Model):
    name = CharField(max_length=40, blank=True, null=True, verbose_name='Название блюда')
    cost = FloatField(blank=True, null=True, verbose_name='Цена')
    weight = FloatField(blank=True, null=True, verbose_name='Вес')
    composition = CharField(max_length=120, blank=True, null=True, verbose_name='Состав')
    category_dish = ForeignKey(CategoryDish, on_delete=PROTECT, related_name='dishes', verbose_name='Категория блюд',
                               blank=True, null=True)
    added_dish = ManyToManyField('self', related_name='additional_dish', blank=True, symmetrical=False,
                                 verbose_name='Дополнительное блюдо', through='dinner.AddedDish')

    def __str__(self):
        return self.name

    @classmethod
    def search(cls, name: str,
               queryset=None):
        """
        Метод поиска по объектам класса Dish

        @param name: (str) Искомое значение
                Строка в любом регистре
        @param queryset: (QuerySet) Использовать готовый queryset для поиска в диапазоне переданной выборки

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


class AddedDish(Model):
    to_dish = ForeignKey(Dish, on_delete=CASCADE, related_name='to_dish_check',
                         verbose_name='К какому блюду прибавляем')
    from_dish = ForeignKey(Dish, on_delete=CASCADE, related_name='from_dish_check',
                           verbose_name='Какое блюдо прибавляем')
    сomplex_dinner = ForeignKey(ComplexDinner, on_delete=CASCADE, related_name='added_dish_for_complex', blank=True,
                                null=True, verbose_name='Принадлежность к комплексному обеду')
    for_complex = BooleanField(default=False, verbose_name='Для комплексного обеда')


class Menu(Model):
    dish = ManyToManyField(Dish, verbose_name='Блюдо', blank=True)
    available_order_date = DateField(unique=True, null=True, blank=True, verbose_name='Меню на день')
    close_order_time = Settings.close_order_time

    # Проверяем доступно ли данное меню для заказа.
    @property
    def available_for_order(self):
        now_time = datetime.datetime.now().strftime('%H.%M')
        if now_time <= self.close_order_time.strftime('%H.%M'):
            return True

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"
