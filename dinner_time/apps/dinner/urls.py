from django.urls import path

from .views import *

app_name = "DINNER"

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),

]
