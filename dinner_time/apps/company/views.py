from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.authentication.utils import create_user_account
from apps.company.serializers import CreateCompanySerializer
from apps.users.models import User


class CreateCompanyView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateCompanySerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        serializer.create_ref_link_for_update_auth_data(obj=user)
        headers = self.get_success_headers(serializer.data)
        serializer.data.pop("password", None)
        serializer.data.pop("username", None)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
