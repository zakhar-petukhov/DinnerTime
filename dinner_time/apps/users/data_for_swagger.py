from drf_yasg.openapi import *

request_invite_users = Schema(type=TYPE_OBJECT,
                              properties={
                                  'tariff': Schema(type=TYPE_INTEGER, title='ID тарифа'),
                                  'emails': Schema(type=TYPE_ARRAY, title='emails',
                                                   items=Items(enum={'email': TYPE_STRING},
                                                               type=TYPE_STRING))
                              })
