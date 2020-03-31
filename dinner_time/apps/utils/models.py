from django.db.models import Model, TimeField
import datetime


class Settings(Model):
    close_order_time = TimeField(default=datetime.time(15, 00), null=True, blank=True,
                                 verbose_name='Окончание действия меню')
