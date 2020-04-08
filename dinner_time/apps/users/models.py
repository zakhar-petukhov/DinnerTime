import phonenumbers
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import *
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class User(AbstractUser, MPTTModel):
    objects = UserManager()

    parent = TreeForeignKey('self', on_delete=CASCADE, verbose_name='Куратор', null=True, blank=True,
                            related_name='childs')

    first_name = CharField(max_length=20, null=True, blank=True, verbose_name='Имя')
    last_name = CharField(max_length=20, null=True, blank=True, verbose_name='Фамилия')
    middle_name = CharField(max_length=20, null=True, blank=True, verbose_name='Отчество')

    phone = CharField(max_length=12, null=True, blank=True, verbose_name='Номер телефона')
    email = EmailField(max_length=30, null=True, blank=True, verbose_name='Email')
    email_verified = BooleanField(default=False, verbose_name='Email подтвержден')

    department = ForeignKey('company.Department', on_delete=PROTECT, related_name='department_user', blank=True,
                            null=True, verbose_name='Департамент')

    is_blocked = BooleanField(default=False, verbose_name='Заблокирован')
    block_date = DateTimeField(null=True, blank=True, verbose_name='Дата блокироваки')

    company_data = OneToOneField('company.Company', on_delete=PROTECT, null=True, blank=True,
                                 related_name='company_user', verbose_name='Компания')

    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True, verbose_name='Создано')
    update_date = DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    # Проеобразуем номер телефона в общий формат
    def get_phone_number(self, phone):
        phone_number = phonenumbers.parse(phone, "RU")
        return f"+{str(phone_number.country_code) + str(phone_number.national_number)}"

    @staticmethod
    def autocomplete_search_fields():
        return 'id', 'username', 'last_name', 'first_name', 'phone'

    @property
    def is_company(self):
        if self.company_data:
            return True

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
