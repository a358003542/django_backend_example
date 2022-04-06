#!/usr/bin/env python
# -*-coding:utf-8-*-

from rest_framework import permissions
from rest_framework import exceptions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.core.permissions import PermissionType, get_or_create_permission


def add_role_permissions(role, model, name='', field_or_id=None,
                         permission_type: PermissionType = PermissionType.view):
    """
    给某个角色增加权限
    """
    permission = get_or_create_permission(model=model, field_or_id=field_or_id,
                                          name=name,
                                          permission_type=permission_type)

    role.group.permissions.add(permission)


def remove_role_permissions(role, model, name='', field_or_id=None,
                            permission_type: PermissionType = PermissionType.view):
    permission = get_or_create_permission(model=model, field_or_id=field_or_id,
                                          name=name,
                                          permission_type=permission_type)

    role.group.permissions.remove(permission)


class SameCompanyPermission(permissions.BasePermission):
    """
    只有公司相同才有权限
    """
    message = 'Not in the same company.'

    def has_object_permission(self, request, view, company):
        """
        """
        login_user_company = request.user.organization.company

        if login_user_company and company and (login_user_company == company):
            return True
        else:
            return False


class OrganizationInvitePermission(permissions.BasePermission):
    message = 'Not have permission to invite people.'

    def has_permission(self, request, view):
        user = request.user

        if user.has_perm('organization.change_organization_invited_by'):
            return True
        else:
            return False

class OrganizationRolesChangePermission(permissions.BasePermission):
    message = 'Not have permission to change roles.'

    def has_permission(self, request, view):
        user = request.user

        if user.has_perm('organization.change_organization_roles'):
            return True
        else:
            return False

class CanChangeRolePermission(permissions.BasePermission):
    message = "Not have permission to change role's permission"

    def has_permission(self, request, view):
        user = request.user

        if user.has_perm('organization.change_role_permission'):
            return True
        else:
            return False


class ModelPermission(permissions.BasePermission):
    """
    基于DjangoModelPermissions修改：
    移除queryset依赖，不过需要在视图类上定义 permission_model_class = Company

    It ensures that the user is authenticated, and has the appropriate
    `add`/`change`/`delete` permissions on the model.
    """

    # Map methods into required permission codes.
    # Override this if you need to also provide 'view' permissions,
    # or if you want to provide custom permission codes.
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    authenticated_users_only = True

    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
                not request.user.is_authenticated and self.authenticated_users_only):
            return False

        assert hasattr(view, 'permission_model_class') is not None, (
            'Cannot apply {} on a view that does not set .permission_model_class'
        ).format(self.__class__.__name__)

        perms = self.get_required_permissions(request.method,
                                              view.permission_model_class)

        return request.user.has_perms(perms)
