from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.dinner.serializers import *


class DishViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    lookup_field = "dish_id"


class DishGroupViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MenuGroup.objects.all()
    serializer_class = DishGroupSerializer
    lookup_field = "dish_group_id"
