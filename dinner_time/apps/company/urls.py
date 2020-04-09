from django.urls import path

from apps.authentication.views import UserChangeRegAuthDataView
from apps.company.views import *

app_name = "COMPANY"

urlpatterns = [
    path('create/', CreateCompanyView.as_view(), name='create_company'),
    path('all/', AllCompaniesView.as_view(), name='detail_company'),
    path('detail/<company_id>/', CompanyDetailView.as_view(), name='all_companies'),
    path('block/<company_id>/', CompanyUpdateBlockView.as_view(), name='block_company'),
    path('delete/<company_id>/', CompanyUpdateDeleteView.as_view(), name='delete_company'),
    path('ref/<str:referral_upid>/change_auth/', UserChangeRegAuthDataView.as_view(), name='company_change_auth_ref'),
]
