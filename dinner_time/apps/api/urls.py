from django.urls import path, include
from rest_framework.authtoken import views

from apps.users.urls import router

app_name = "API"

urlpatterns = [
    path('', include(router.urls)),
    path('api_token_auth/', views.obtain_auth_token, name='api_token_auth'),
]
