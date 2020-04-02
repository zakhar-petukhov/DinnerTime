from django.urls import path

from apps.company.views import CreateCompanyView, UserChangeRegAuthDataView, AllCompaniesView, RemoveCompaniesView

app_name = "COMPANY"

urlpatterns = [
    path('create/', CreateCompanyView.as_view(), name='create_company'),
    path('all/', AllCompaniesView.as_view(), name='all_companies'),
    path('remove/<company_id>/', RemoveCompaniesView.as_view(), name='remove_company'),
    path('ref/<str:referral_upid>/change_auth/', UserChangeRegAuthDataView.as_view(), name='company_change_auth_ref'),
]
