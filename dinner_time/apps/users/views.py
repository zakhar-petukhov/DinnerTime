from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.authentication.utils import create_user_account, generate_random_username_password
from apps.users.permissions import IsCompanyAuthenticated
from apps.users.serializers import *

User = get_user_model()


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DepartmentViewSet(GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsCompanyAuthenticated]
    serializer_class = EmptySerializer
    serializer_classes = {
        'create_department': DepartmentSerializer,
        'add_user': UserCreateSerializer,
        'list': DepartmentSerializer,
    }

    # Create department
    @action(methods=['POST'], detail=False)
    def create_department(self, request, *args, **kwargs):
        request.data['company'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Create and add user into department
    @action(methods=['POST'], detail=False)
    def add_user(self, request):
        parent = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update(generate_random_username_password())
        create_user_account(parent=parent, **serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    method_serializer_classes = get_serializer_class

    def get_object(self):
        departament_id = self.kwargs["pk"]
        obj = get_object_or_404(Department, pk=departament_id)
        return obj

    def get_queryset(self):
        employee_id = self.request.user.id
        return Department.objects.filter(company_id=employee_id)
