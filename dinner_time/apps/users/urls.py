from rest_framework import routers

from apps.users.views import *

app_name = "USERS"

router = routers.DefaultRouter()
router.register('user', UserView, base_name='user_api')

urlpatterns = [

]
