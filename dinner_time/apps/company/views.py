from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.authentication.utils import create_user_account
from apps.company.models import ReferralLink
from apps.company.serializers import CreateCompanySerializer, ChangeRegAuthDataSerializer
from apps.users.models import User
from apps.utils.func_for_send_message import send_message_for_change_auth_data


class CreateCompanyView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateCompanySerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(is_company=True, **serializer.validated_data)
        upid = serializer.create_ref_link_for_update_auth_data(obj=user)
        headers = self.get_success_headers(serializer.data)

        url = settings.URL_FOR_CHANGE_AUTH_DATA.format(upid)
        header, body = send_message_for_change_auth_data(url=url, company_name=serializer.data.get('company_name'))
        email = EmailMessage(header, body, to=[serializer.data.get('email')])
        email.send()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserChangeRegAuthDataView(UpdateAPIView):
    serializer_class = ChangeRegAuthDataSerializer
    model = User
    permission_classes = ()

    def get_object(self):
        upid = self.kwargs["referral_upid"]
        obj = get_object_or_404(ReferralLink, upid=upid, is_active=True)

        return obj

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if User.objects.filter(username=serializer.data.get("username")).exists():
                raise serializers.ValidationError(
                    "Такой username уже занят, пожалуйста, введите другой и повторите запрос.")

            obj.user.set_password(serializer.data.get("password"))
            obj.is_active = False
            obj.user.save()
            obj.save()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
