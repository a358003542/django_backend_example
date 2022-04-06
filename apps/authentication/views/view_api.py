#!/usr/bin/env python
# -*-coding:utf-8-*-

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.organization.permissions import SameCompanyPermission
from apps.authentication.renderers import UserJSONRenderer, ProfileJSONRenderer
from apps.authentication.serializers import PhoneLoginSerializer, \
    ProfileSerializer, UserSerializer, RegistrationSerializer, LoginSerializer
from apps.authentication.models import Profile


class PhoneLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = PhoneLoginSerializer

    def post(self, request, ):
        """
        手机登录附带自动注册过程

        """
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    """
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        用户注册需要提供用户名+邮箱+密码

        注册接口单独写，基本上任何人都可以注册。
        """
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        """
        用户登录

        用户登录单独编写，基本上任何人都可以访问。
        登录 用户名或邮箱都可
        """
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """
        用户获取自己的一些信息

        也包括自己的档案信息和组织信息
        """
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        用户修改自己的信息

        不能修改自己的组织信息
        """
        user_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=user_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated, SameCompanyPermission)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def get(self, request, username, *args, **kwargs):
        """
        用户更喜欢接受url上有自己的用户名

        查看其他用户的档案信息

        暂定为相同的公司都可以彼此查看彼此的档案信息
        """
        try:
            queryset = Profile.objects.select_related('user')
            profile = queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist.')

        # same company check
        self.check_object_permissions(request,
                                      profile.user.organization.company)

        serializer = self.serializer_class(profile, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
