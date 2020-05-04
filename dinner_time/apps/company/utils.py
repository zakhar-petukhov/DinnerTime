from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response

from apps.users.utils import *
from apps.utils.func_for_send_message import send_message_for_change_auth_data_client


def create_user_or_company(company_name, serializer, parent=None):
    serializer.validated_data.update(generate_random_password_username())

    user = create_user_account(parent=parent, **serializer.validated_data)
    upid = create_ref_link_for_update_auth_data(obj=user)

    send_message(company_name, upid, serializer.data)

    return Response(status=status.HTTP_201_CREATED)


def send_message(company_name, upid, data):
    url = settings.URL_FOR_CHANGE_AUTH_DATA.format(upid)

    header, body = send_message_for_change_auth_data_client(url=url,
                                                            company_name=company_name)
    email = EmailMessage(header, body, to=[data.get('email')])
    email.send()
