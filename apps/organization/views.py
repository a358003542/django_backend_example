import logging

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Organization, Company, Department, Role
from .renderers import OrganizationJSONRenderer, CompanyJsonRenderer, \
    DepartmentJsonRenderer, RuleJSONRenderer
from .serializers import OrganizationSerializer, CompanySerializer, \
    DepartmentSerializer, RoleSerializer
from apps.authentication.models import User
from apps.organization.permissions import SameCompanyPermission, \
    ModelPermission, OrganizationInvitePermission, \
    OrganizationRolesChangePermission, CanChangeRolePermission




logger = logging.getLogger(__name__)


class OrganizationAPIView(APIView):
    """
    本人查看本人的组织信息

    """
    permission_classes = (IsAuthenticated)
    renderer_classes = (OrganizationJSONRenderer,)
    serializer_class = OrganizationSerializer

    def get(self, request, *args, **kwargs):
        """
        查看自己的组织信息
        """
        try:
            queryset = Organization.objects.select_related('user')
            organization = queryset.get(user__username=request.user.username)
        except Organization.DoesNotExist:
            raise NotFound('Organization with this username does not exist.')

        serializer = self.serializer_class(organization)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganizationOtherAPIView(APIView):
    """
    组织

    """
    permission_classes = (
        IsAuthenticated, SameCompanyPermission, ModelPermission)
    renderer_classes = (OrganizationJSONRenderer,)
    serializer_class = OrganizationSerializer
    permission_model_class = Organization


    def get(self, request, username, *args, **kwargs):
        """
        查看其他用户的组织信息

        只有本公司内才能查看
        """
        try:
            queryset = Organization.objects.select_related('user')
            organization = queryset.get(user__username=username)
        except Organization.DoesNotExist:
            raise NotFound('Organization with this username does not exist.')

        # same company check
        self.check_object_permissions(request, organization.company)

        serializer = self.serializer_class(organization)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, username, *args, **kwargs):
        """
        修改其他用户的组织信息

        相同公司 需要有Organization模型的change权限
        """
        try:
            queryset = Organization.objects.select_related('user')
            organization = queryset.get(user__username=username)
        except Organization.DoesNotExist:
            raise NotFound('Organization with this username does not exist.')

        # same company check
        self.check_object_permissions(request, organization.company)

        organization_data = request.data.get('organization', {})

        serializer = self.serializer_class(organization, data=organization_data,
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganizationRoleAddAPIView(APIView):
    """


    """
    permission_classes = (
        IsAuthenticated, SameCompanyPermission,
        OrganizationRolesChangePermission)
    renderer_classes = (OrganizationJSONRenderer,)
    serializer_class = OrganizationSerializer

    def post(self, request, username, role_name, *args, **kwargs):
        """
        将用户添加进某个角色
        """
        try:
            queryset = Organization.objects.select_related('user')
            organization = queryset.get(user__username=username)
        except Organization.DoesNotExist:
            raise NotFound('Organization with this username does not exist.')

        # same company check
        self.check_object_permissions(request, organization.company)

        try:
            target_role = Role.objects.get(name=role_name,
                                           company=organization.company)
        except Role.DoesNotExist:
            raise NotFound('Role with this name does not exist.')

        organization.roles.add(target_role)

        return Response({'info': 'ok'}, status=status.HTTP_200_OK)


class OrganizationRoleRemoveAPIView(APIView):
    """

    """
    permission_classes = (
        IsAuthenticated, SameCompanyPermission,
        OrganizationRolesChangePermission)
    renderer_classes = (OrganizationJSONRenderer,)
    serializer_class = OrganizationSerializer

    def post(self, request, username, role_name, *args, **kwargs):
        """
        将用户移除出某个角色
        """
        try:
            queryset = Organization.objects.select_related('user')
            organization = queryset.get(user__username=username)
        except Organization.DoesNotExist:
            raise NotFound('Organization with this username does not exist.')

        # same company check
        self.check_object_permissions(request, organization.company)

        try:
            target_role = Role.objects.get(name=role_name,
                                           company=organization.company)
        except Role.DoesNotExist:
            raise NotFound('Role with this name does not exist.')

        organization.roles.remove(target_role)

        return Response({'info': 'ok'}, status=status.HTTP_200_OK)



class CompanyAPIView(APIView):
    """
    公司信息

    """
    permission_classes = (IsAuthenticated, ModelPermission)
    renderer_classes = (CompanyJsonRenderer,)
    serializer_class = CompanySerializer
    permission_model_class = Company

    def get(self, request, *args, **kwargs):
        """
        获取用户当前所在的公司的公司信息

        """
        serializer = self.serializer_class(request.user.organization.company)

        return Response(serializer.data, status.HTTP_200_OK)


    def patch(self, request, *args, **kwargs):
        """
        修改用户当前所在公司的公司信息

        登录用户并且有Company的change权限
        """
        company = request.user.organization.company
        company_data = request.data.get('company', {})

        serializer = self.serializer_class(company, data=company_data,
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        增加公司

        登录用户并且有Company模型的add权限
        NOTICE： 不开放put方法，增加公司权限会有特别的限制
        """
        company = request.data.get('company', {})
        serializer = self.serializer_class(data=company)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class CompanyOtherAPIView(APIView):
    """

    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CompanyJsonRenderer,)
    serializer_class = CompanySerializer

    def get(self, request, company_name, *args, **kwargs):
        """
        获取公司信息

        """
        try:
            target_company = Company.objects.get(name=company_name)
        except Company.DoesNotExist:
            raise NotFound('Company with this company_name does not exist.')

        serializer = self.serializer_class(target_company)

        return Response(serializer.data, status.HTTP_200_OK)


class DepartmentAPIView(APIView):
    """
    部门信息

    增加部门 登录用户 并且有Department的add权限

    """
    permission_classes = (IsAuthenticated, ModelPermission)
    renderer_classes = (DepartmentJsonRenderer,)
    serializer_class = DepartmentSerializer
    permission_model_class = Department

    def post(self, request, *args, **kwargs):
        """
        增加部门

        请求格式 {'department': {'name': ...}}
        """
        user = request.user

        try:
            organization = Organization.objects.get(user=user.pk)
        except Organization.DoesNotExist:
            raise NotFound('Organization with this username does not exist.')

        department = request.data.get('department', {})

        serializer = self.serializer_class(data=department, context={
            'company_name': organization.company.name
        })

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class OrganizationInviteAPIView(APIView):
    """
    邀请某个用户加入公司
    """
    permission_classes = (IsAuthenticated, OrganizationInvitePermission)
    renderer_classes = (OrganizationJSONRenderer,)
    serializer_class = OrganizationSerializer

    def patch(self, request, username, *args, **kwargs):
        """
        邀请某个用户加入公司

        # 需要本用户有 can_invite_people 权限
        """
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('User with this username does not exist.')

        target_user.organization.invited_by = request.user.organization.company.name
        target_user.organization.save()

        return Response({'info': 'ok'}, status=status.HTTP_200_OK)


class OrganizationAcceptInviteAPIView(APIView):
    """

    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (OrganizationJSONRenderer,)
    serializer_class = OrganizationSerializer

    def patch(self, request, company_name, *args, **kwargs):
        """
        用户接受某个公司的邀请
        """
        result = {}
        # 首先确认本用户已经被公司邀约了
        invited_by_company_name = request.user.organization.invited_by
        if invited_by_company_name:
            if invited_by_company_name == company_name:
                try:
                    target_company = Company.objects.get(name=company_name)
                    request.user.organization.company = target_company
                    request.user.organization.save()
                    result['info'] = 'ok'
                except Company.DoesNotExist:
                    result['info'] = '目标公司名并不存在'
            else:
                result['info'] = '邀约公司和接受邀约公司并不相同'
        else:
            result['info'] = '用户并没有被公司邀约'

        return Response(result, status=status.HTTP_200_OK)


class RoleAPIView(APIView):
    permission_classes = (IsAuthenticated, ModelPermission)
    renderer_classes = (RuleJSONRenderer,)
    serializer_class = RoleSerializer
    permission_model_class = Role

    def post(self, request, *args, **kwargs):
        """
        增加一个新的角色
        """
        user = request.user

        try:
            organization = Organization.objects.get(user=user)
        except Organization.DoesNotExist:
            raise NotFound('Organization with this user does not exist.')

        role_data = request.data.get('role', {})

        serializer = self.serializer_class(data=role_data, context={
            'company_name': organization.company.name
        })

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class RoleAddPermissionAPIView(APIView):
    permission_classes = (IsAuthenticated, CanChangeRolePermission)
    renderer_classes = (RuleJSONRenderer,)
    serializer_class = RoleSerializer

    def post(self, request, role_id, *args, **kwargs):
        """
        角色增加权限

        {
            'model': 'app_label.model_name'
        }
        """
        permission_data = request.data.get('permission', {})

        try:
            target_role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            raise NotFound('Role with this id does not exist.')

        from .permissions import add_role_permissions

        model = permission_data.get('model')
        name = permission_data.get('name', '')
        field_or_id = permission_data.get('field_or_id', None)
        permission_type = permission_data.get('permission_type')

        from apps.core.permissions import PermissionTypeDict
        assert permission_type in PermissionTypeDict
        permission_type = PermissionTypeDict[permission_type]

        result = {}
        add_role_permissions(target_role, model, name=name,
                             field_or_id=field_or_id,
                             permission_type=permission_type)
        result['info'] = 'ok'
        return Response(result, status.HTTP_200_OK)


class RoleRemovePermissionAPIView(APIView):
    permission_classes = (IsAuthenticated, CanChangeRolePermission)
    renderer_classes = (RuleJSONRenderer,)
    serializer_class = RoleSerializer

    def post(self, request, role_id, *args, **kwargs):
        """

        """
        permission_data = request.data.get('permission', {})

        try:
            target_role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            raise NotFound('Role with this id does not exist.')

        from .permissions import remove_role_permissions

        model = permission_data.get('model')
        name = permission_data.get('name', '')
        field_or_id = permission_data.get('field_or_id', None)
        permission_type = permission_data.get('permission_type')

        from apps.core.permissions import PermissionTypeDict
        assert permission_type in PermissionTypeDict
        permission_type = PermissionTypeDict[permission_type]

        result = {}
        remove_role_permissions(target_role, model, name=name,
                                field_or_id=field_or_id,
                                permission_type=permission_type)
        result['info'] = 'ok'
        return Response(result, status.HTTP_200_OK)


class RoleCategoryAPIView(APIView):
    pass
