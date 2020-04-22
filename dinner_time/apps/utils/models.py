import datetime
import secrets

from config_models.models import ConfigurationModel
from django.conf import settings
from django.db.models import *
from django.db.models import Model

from apps.users.models import User


class Settings(ConfigurationModel):
    close_order_time = TimeField(default=datetime.time(15, 00), verbose_name='Окончание действия меню')


class ReferralLink(Model):
    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)

    upid = CharField(max_length=43, unique=True, null=True, blank=True, verbose_name='UPID')
    user = ForeignKey(User, on_delete=CASCADE, related_name='ref_link', blank=True, null=True,
                      verbose_name='Пользователь')
    is_active = BooleanField(default=True, verbose_name='Активность ссылки')

    def __str__(self):
        return settings.REFERRAL_BASE_URL + f'/{self.pk}/'

    # Genarate UPID
    @classmethod
    def get_generate_upid(self):
        upid = secrets.token_urlsafe()
        return upid

    class Meta:
        verbose_name = 'Реферальная ссылка'
