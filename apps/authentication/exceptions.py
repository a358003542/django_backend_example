#!/usr/bin/env python
# -*-coding:utf-8-*-

from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class ProfileDoesNotExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The requested profile does not exist.'
    default_code = 'profile_does_not_exists'

class UserAlreadyExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('User already exist.')
    default_code = 'user_already_exist'