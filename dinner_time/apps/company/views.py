from datetime import datetime

import pytz
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework import filters
from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.utils import create_user_account, generate_random_username_password, \
    create_ref_link_for_update_auth_data
from apps.company.serializers import CreateCompanySerializer, ChangeRegAuthDataSerializer, \
    GetInformationCompanySerializer
from apps.users.models import User
from apps.utils.func_for_send_message import send_message_for_change_auth_data_company
from apps.utils.models import ReferralLink


class CreateCompanyView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateCompanySerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update(generate_random_username_password())
        company = create_user_account(**serializer.validated_data)

        upid = create_ref_link_for_update_auth_data(obj=company)
        headers = self.get_success_headers(serializer.data)

        url = settings.URL_FOR_CHANGE_AUTH_DATA.format(upid)
        header, body = send_message_for_change_auth_data_company(url=url,
                                                                 company_name=serializer.data.get('company_name'))
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


class AllCompaniesView(ListAPIView):
    queryset = User.objects.filter(is_company=True)
    serializer_class = GetInformationCompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_name']
    permission_classes = [IsAdminUser]


class RemoveCompaniesView(APIView):
    def delete(self, request, company_id):
        company = User.objects.get(id=company_id)

        if request.user.is_superuser:
            company.is_blocked = True
            company.block_date = datetime.now(pytz.timezone(settings.TIME_ZONE))
            company.save()

            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        else:
            return HttpResponseBadRequest()
