from django.urls import path

from apps.company.views import CreateCompanyView, UserChangeRegAuthDataView

app_name = "COMPANY"

urlpatterns = [
    path('create/', CreateCompanyView.as_view(), name='create_company'),
    path('ref/<str:referral_upid>/change_auth/', UserChangeRegAuthDataView.as_view(), name='company_change_auth_ref'),
]
