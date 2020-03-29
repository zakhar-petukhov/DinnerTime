import datetime

from django.db.models import *

from apps.users.models import User


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


class MenuGroup(Model):
    name = CharField(max_length=40, blank=True, null=True, verbose_name='Название группы')

    def __str__(self):
        return self.name


class Dish(Model):
    name = CharField(max_length=40, blank=True, null=True, verbose_name='Название блюда')
    cost = FloatField(blank=True, null=True, verbose_name='Цена')
    weight = FloatField(blank=True, null=True, verbose_name='Вес')
    composition = CharField(max_length=120, blank=True, null=True, verbose_name='Состав')
    menu_group = ForeignKey(MenuGroup, on_delete=PROTECT, related_name='dishes', verbose_name='Группа меню',
                            blank=True, null=True)
    added_dish = ForeignKey('self', on_delete=PROTECT, related_name='additional_menu',
                            verbose_name='Дополнительное блюдо', blank=True, null=True)

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


class Menu(Model):
    dish = ManyToManyField(Dish, verbose_name='Блюдо', blank=True)
    available_order_date = DateField(unique=True, null=True, blank=True, verbose_name='Меню на день')
    # TODO вынести настройки
    close_order_time = TimeField(default=datetime.time(15, 00), null=True, blank=True,
                                 verbose_name='Окончание действия меню')

    # Проверяем доступно ли данное меню для заказа.
    @property
    def available_for_order(self):
        pass

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"
