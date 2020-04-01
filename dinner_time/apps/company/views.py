from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.authentication.utils import create_user_account
from utils.func_for_send_message import send_message_for_change_auth_data
from apps.company.serializers import CreateCompanySerializer
from apps.users.models import User


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
