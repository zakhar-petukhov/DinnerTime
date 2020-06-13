from django.urls import path
from rest_framework import routers

from apps.authentication.views import UserChangeRegAuthDataView
from apps.common.views import ImageViewSet
from apps.users.views import *

app_name = "USERS"

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, base_name='user')
router.register(r'image', ImageViewSet, base_name='user_image')

urlpatterns = [
    path('ref/<str:referral_upid>/change_auth/', UserChangeRegAuthDataView.as_view(), name='user_change_auth_ref'),

    path('create/dinner/', UserCreateDinnerView.as_view({'post': 'create'}), name='user_add_dish'),

    path('create/tariff/', TariffCreateView.as_view({'post': 'create'}), name='create_tariff'),
    path('change/tariff/<tariff_id>/', TariffCreateView.as_view({'put': 'update'}), name='change_tariff'),
    path('list/all_tariff/', TariffCreateView.as_view({'get': 'list'}), name='list_all_tariff'),

    path('invite/users/', InviteUsersView.as_view(), name='invite_user'),

    *router.urls
]
