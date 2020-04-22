from django.urls import path

from apps.utils.views import SettingsViewSet

app_name = "UTILS"

urlpatterns = [
    path('change_settings/<settings_id>', SettingsViewSet.as_view({'put': 'update'}), name='change_settings'),
    path('list_all_settings/', SettingsViewSet.as_view({'get': 'list'}), name='list_all_settings'),
]
