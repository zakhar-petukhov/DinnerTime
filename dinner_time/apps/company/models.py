import secrets

from django.conf import settings
from django.db.models import *

from apps.users.models import User


class ReferralLink(Model):
    create_date = DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)

    upid = CharField(max_length=43, unique=True, null=True, blank=True, verbose_name='UPID')
    user = ForeignKey(User, on_delete=CASCADE, related_name='ref_link', blank=True, null=True,
                      verbose_name='Пользователь')
    is_active = BooleanField(default=True, verbose_name='Активность ссылки')

    def __str__(self):
        return settings.REFERRAL_BASE_URL + f'/{self.pk}/'

    # Генерируем UPID
    @classmethod
    def get_generate_upid(self):
        upid = secrets.token_urlsafe()
        return upid

    class Meta:
        verbose_name = 'Реферальная ссылка'
