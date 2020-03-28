from django.contrib.auth import get_user_model
from rest_framework import viewsets

from apps.users.serializers import UserSerializers

User = get_user_model()


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
