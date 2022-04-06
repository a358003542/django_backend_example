#!/usr/bin/env python
# -*-coding:utf-8-*-

from django.test import testcases
from apps.core.renderers import explainErrorDetail
from rest_framework.exceptions import ErrorDetail
from apps.core.nested_dict import nested_dict_from_dict, nested_dict
from rest_framework.test import APITestCase
from apps.authentication.models import User
from unittest import skip
from django.urls import reverse


class TestRenderersDetail(testcases.TestCase):
    def test_explain_ErrorDetail(self):
        test_dict = {'errors': {'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated')}}
        explainErrorDetail(test_dict)

    def test_nested_dict(self):
        from collections import OrderedDict

        data = {'user': {'email': 'lucy@django.com', 'username': 'lucy',
                         'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTMwLCJleHAiOjE2NDY2MzcxMzJ9.kUacB3R8YFeaCT6zJ_Zas9tkO_8_RPU407lNPAmWeAI',
                         'profile': OrderedDict(
                             [('username', 'lucy'), ('bio', ''), (
                                 'image',
                                 'https://static.productionready.io/images/smiley-cyrus.jpg')])}}

        res = nested_dict()
        nested_dict_from_dict(data, res)
        ret_data = res.to_dict()

        self.assertEqual(ret_data['user']['profile']['username'], 'lucy')


class TestUploadImage(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="lucy",
                                             password="343433353",
                                             email="lucy@django.com")

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "lucy@django.com",
                "password": "343433353"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    @skip("has tested")
    def test_upload_image(self):
        with open('./examples/test.jpg', 'rb') as f:
            response = self.client.put(
                reverse('api-upload-image', kwargs={'filename': 'test.jpg'}),
                data=f.read(),
                content_type='image/jpg')

            print(response.data)


class TestUploadFile(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="lucy",
                                             password="343433353",
                                             email="lucy@django.com")

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "lucy@django.com",
                "password": "343433353"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    @skip("has tested")
    def test_upload_file(self):
        with open('./examples/test.txt', 'rb') as f:
            response = self.client.put(
                reverse('api-upload-file', kwargs={'filename': 'test.txt'}),
                data=f.read(),
                content_type='text/plain')

            print(response.data)
