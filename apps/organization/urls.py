#!/usr/bin/env python
# -*-coding:utf-8-*-


from django.urls import path

from .views import OrganizationOtherAPIView, CompanyAPIView, \
    DepartmentAPIView, \
    RoleAPIView, RoleCategoryAPIView, OrganizationAPIView, CompanyOtherAPIView, \
    OrganizationInviteAPIView, OrganizationAcceptInviteAPIView, \
    OrganizationRoleAddAPIView, OrganizationRoleRemoveAPIView, \
    RoleAddPermissionAPIView, RoleRemovePermissionAPIView

urlpatterns = [
    path('api/organization/', OrganizationAPIView.as_view(),
         name='api-self-organization'),
    path('api/organization/<username>/', OrganizationOtherAPIView.as_view(),
         name='api-other-organization'),
    path('api/organization/<username>/roles/add/<role_name>/',
         OrganizationRoleAddAPIView.as_view(),
         name='api-organization-add-role'),
    path('api/organization/<username>/roles/remove/<role_name>/',
         OrganizationRoleRemoveAPIView.as_view(),
         name='api-organization-remove-role'),

    # 将某个用户拉入公司 必须是公司具有特殊权限的对某个用户发出邀请
    # 并且最终用户点击接受用户才算是加入该公司
    path('api/invite/<username>/',
         OrganizationInviteAPIView.as_view(), name='api-invite-user'),
    path('api/accept_invite/<company_name>/',
         OrganizationAcceptInviteAPIView.as_view(), name='api-accept-invite'),

    path('api/company/', CompanyAPIView.as_view(), name='api-company'),

    path('api/company/<company_name>/', CompanyOtherAPIView.as_view(),
         name='api-other-get-company'),

    path('api/department/', DepartmentAPIView.as_view(),
         name='api-new-department'),
    path('api/role/', RoleAPIView.as_view(), name='api-new-role'),
    path('api/role/<role_id>/add-permission/',
         RoleAddPermissionAPIView.as_view(), name='api-role-add-permission'),
    path('api/role/<role_id>/remove-permission/',
         RoleRemovePermissionAPIView.as_view(),
         name='api-role-remove-permission'),
    # path('role_category/', RoleCategoryAPIView.as_view())
]
