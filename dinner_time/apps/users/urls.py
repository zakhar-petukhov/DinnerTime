from django.urls import path
from rest_framework import routers

from apps.authentication.views import UserChangeRegAuthDataView
from apps.users.views import *

app_name = "USERS"

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, base_name='user')

urlpatterns = [
    path('ref/<str:referral_upid>/change_auth/', UserChangeRegAuthDataView.as_view(), name='user_change_auth_ref'),
    *router.urls
]
