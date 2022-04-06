#!/usr/bin/env python
# -*-coding:utf-8-*-

from django.urls import path

import apps.authentication.views.view_web as view_web

from .views.view_api import PhoneLoginAPIView, RegistrationAPIView, \
    LoginAPIView, UserAPIView, ProfileAPIView

urlpatterns = [
    path('api/user/registration/', RegistrationAPIView.as_view(),
         name='api-registration'),
    path('api/user/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/user/phone-login/', PhoneLoginAPIView.as_view(),
         name='api-phone-login'),
    path('api/user/', UserAPIView.as_view(), name='api-user'),
    path('api/profiles/<username>/', ProfileAPIView.as_view(),
         name='api-profile'),

    # web
    path("", view_web.home, name="home"),
]
