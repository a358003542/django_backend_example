from datetime import datetime
from unittest import skip
from django.urls import reverse
from .models import User
from rest_framework.test import APITestCase
from apps.organization.models import Company


class UserRegistrationTestCase(APITestCase):
    def test_registration(self):
        response = self.client.post(reverse('api-registration'), {
            "user": {
                "username": "abc",
                "email": "abc@django.com",
                "password": "3435545343"
            }
        })
        self.assertEqual(response.data['user']['email'], 'abc@django.com')
        self.assertEqual(response.data['user']['username'], 'abc')

        user = User.objects.get(username='abc')
        self.assertEqual(user.email, 'abc@django.com')


class UserLoginTestCase(APITestCase):
    """
    邮箱登录
    """

    def setUp(self):
        User.objects.create_user(username="lion", password="123343455",
                                 email="lion@django.com")

    def test_user_exists(self):
        lion = User.objects.get(username="lion")
        self.assertEqual(lion.username, 'lion')

    def test_user_login(self):
        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "lion@django.com",
                "password": "123343455"
            }
        })

        self.assertIn('token', response.data['user'])


class UserLoginTestCase2(APITestCase):
    """
    用户名登录
    """

    def setUp(self):
        User.objects.create_user(username="lion", password="123343455",
                                 email="lion@django.com")

    def test_user_login(self):
        response = self.client.post(reverse('api-login'), {
            "user": {
                "username": "lion",
                "password": "123343455"
            }
        })

        self.assertIn('token', response.data['user'])


class UserLoginTestCase3(APITestCase):
    """
    手机登录
    """

    @skip("phone login has tested.")
    def test_user_login(self):
        response = self.client.post(reverse('api-phone-login'), {
            "user": {
                "phone": "13257429565",
                "biz_id": "self.biz_id",
                "send_date": datetime.now().strftime('%Y%m%d'),
                'verification_code': '1234'
            }
        })

        self.assertIn('token', response.data['user'])

        user = User.objects.get(phone='13257429565')


class GetUserInfoTestCase(APITestCase):
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

    def test_get_user_info(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.get(reverse('api-user'))

        self.assertEqual(response.data['user']['email'], 'lucy@django.com')
        self.assertEqual(response.data['user']['profile']['image'],
                         'https://static.productionready.io/images/smiley-cyrus.jpg')


class UpdateUserInfoTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="before_updated_user",
                                             password="5656565",
                                             email="before_updated_user@django.com")

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "before_updated_user@django.com",
                "password": "5656565"
            }
        })
        self.token = response.data['user']['token']

    def test_update_user_info(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(reverse('api-user'), data={
            'user': {
                'username': 'after_updated_user',
                'email': 'after_updated_user@django.com'
            }
        })

        self.assertEqual(response.data['user']['username'],
                         'after_updated_user')
        self.assertEqual(response.data['user']['email'],
                         'after_updated_user@django.com')

    def test_update_user_info_token_wrong(self):
        token = 'wrong token'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.patch(reverse('api-user'), data={
            'user': {
                'username': 'after_updated_user',
                'email': 'after_updated_user@django.com'
            }
        })

        self.assertEqual(response.status_code, 403)


class ProfileAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="lucy",
                                             password="343433353",
                                             email="lucy@django.com")

        self.user2 = User.objects.create_user(username="lucy2",
                                              password="343433353",
                                              email="lucy2@django.com")

        # save company
        self.company_self = Company.objects.create(name='测试公司2')
        self.user.organization.company = self.company_self
        self.user.organization.save()
        self.user2.organization.company = self.company_self
        self.user2.organization.save()

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "lucy@django.com",
                "password": "343433353"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_other_user_profile(self):
        """
        必须是相同的公司
        """
        response = self.client.get(
            reverse('api-profile', kwargs={'username': 'lucy2'}))

        self.assertEqual(response.data['profile']['username'], 'lucy2')
