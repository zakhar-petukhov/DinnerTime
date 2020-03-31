from django.urls import path

from apps.company.views import CreateCompanyView

app_name = "COMPANY"

urlpatterns = [
    path('create/', CreateCompanyView.as_view(), name='create_company'),
]
