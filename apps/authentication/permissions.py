#!/usr/bin/env python
# -*-coding:utf-8-*-


from rest_framework import permissions
from rest_framework import exceptions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.core.permissions import PermissionType, get_permission_codename


