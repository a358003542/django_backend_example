from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.test import APITestCase
from apps.authentication.models import User
from apps.organization.models import Company, Organization, Department
from apps.core.permissions import PermissionType, add_user_permissions, \
    add_user_basic_model_permissions


class OrganizationGetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_organization_get",
                                             password="456565",
                                             email="test_organization_get@django.com")
        self.user_other = User.objects.create_user(
            username="test_organization_other",
            password="456565",
            email="test_organization_other@django.com")
        self.company_self = Company.objects.create(name='测试公司2')
        self.company_other = Company.objects.create(name='测试公司3')

        self.user.organization.company = self.company_self
        self.user_other.organization.company = self.company_other
        self.user.organization.save()
        self.user_other.organization.save()

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "test_organization_get@django.com",
                "password": "456565"
            }
        })

        self.token = response.data['user']['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_organization_get_right(self):
        response = self.client.get(reverse('api-other-organization', kwargs={
            'username': 'test_organization_get'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['organization']['company']['name'],
                         '测试公司2')

    def test_organization_get_wrong(self):
        response = self.client.get(reverse('api-other-organization', kwargs={
            'username': 'test_organization_other'}))

        self.assertEqual(response.data['errors']['detail']['code'],
                         'permission_denied')


class OrganizationPatchTestCase(APITestCase):
    """
    无权限
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test_organization_put",
                                             password="456565",
                                             email="test_organization_put@django.com")
        self.user_other = User.objects.create_user(
            username="test_organization_put_other",
            password="456565",
            email="test_organization_put_other@django.com")
        self.company_self = Company.objects.create(name='测试公司put2')

        self.user.organization.company = self.company_self
        self.user_other.organization.company = self.company_self
        self.user.organization.save()
        self.user_other.organization.save()

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "test_organization_put@django.com",
                "password": "456565"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_organization_patch_no_permission(self):
        response = self.client.patch(
            reverse('api-other-organization',
                    kwargs={'username': 'test_organization_put_other'}),
            {
                'organization': {
                    'position': '人事部'
                }
            })

        self.assertEqual(response.data['errors']['detail']['code'],
                         'permission_denied')


class OrganizationPatchTestCase2(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_organization_put2",
                                             password="456565",
                                             email="test_organization_put2@django.com")
        self.user_other = User.objects.create_user(
            username="test_organization_put_other2",
            password="456565",
            email="test_organization_put_other2@django.com")
        self.company_self = Company.objects.create(name='测试公司put3')

        self.user.organization.company = self.company_self
        self.user_other.organization.company = self.company_self
        self.user.organization.save()
        self.user_other.organization.save()

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "test_organization_put2@django.com",
                "password": "456565"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_organization_patch_right(self):
        add_user_basic_model_permissions(self.user, Organization,
                                         PermissionType.change)

        self.user = get_object_or_404(User, pk=self.user.pk)

        response = self.client.patch(
            reverse('api-other-organization',
                    kwargs={'username': 'test_organization_put_other2'}),
            {
                'organization': {
                    'position': 'python研发工程师',
                }
            })

        self.assertEqual(response.data['organization']['position'],
                         'python研发工程师')


class CompanyPOSTTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_company_post",
                                             password="456565",
                                             email="test_company_post@django.com")

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "test_company_post@django.com",
                "password": "456565"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_company_post(self):
        add_user_basic_model_permissions(self.user, Company,
                                         PermissionType.add)
        self.user = get_object_or_404(User, pk=self.user.pk)

        response = self.client.post(reverse('api-company'),
                                    {
                                        'company': {
                                            'name': '测试post公司'
                                        }
                                    })

        self.assertEqual(response.data['company']['name'], '测试post公司')


class CompanyGETTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_company_post",
                                             password="456565",
                                             email="test_company_post@django.com")

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "test_company_post@django.com",
                "password": "456565"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        add_user_basic_model_permissions(self.user, Company,
                                         PermissionType.add)
        self.user = get_object_or_404(User, pk=self.user.pk)
        response = self.client.post(reverse('api-company'),
                                    {
                                        'company': {
                                            'name': '测试post公司'
                                        }
                                    })

    def test_company_get(self):
        """
        """
        response = self.client.get(reverse('api-company'))

        self.assertTrue(not response.data['company']['name'])


class CompanyGETTestCase2(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_company_post",
                                             password="456565",
                                             email="test_company_post@django.com")

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "test_company_post@django.com",
                "password": "456565"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        add_user_basic_model_permissions(self.user, Company,
                                         PermissionType.add)
        self.user = get_object_or_404(User, pk=self.user.pk)
        response = self.client.post(reverse('api-company'),
                                    {
                                        'company': {
                                            'name': '测试post公司'
                                        }
                                    })

        target_company = Company.objects.get(name='测试post公司')
        self.user.organization.company = target_company
        self.user.organization.save()

    def test_company_get(self):
        """
        """
        response = self.client.get(reverse('api-company'))

        self.assertEqual(response.data['company']['name'], '测试post公司')


class CompanyPatchTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_company_post",
                                             password="456565",
                                             email="test_company_post@django.com")

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "test_company_post@django.com",
                "password": "456565"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        add_user_basic_model_permissions(self.user, Company,
                                         PermissionType.add)
        add_user_basic_model_permissions(self.user, Company,
                                         PermissionType.change)

        self.user = get_object_or_404(User, pk=self.user.pk)
        response = self.client.post(reverse('api-company'),
                                    {
                                        'company': {
                                            'name': '测试post公司'
                                        }
                                    })

        target_company = Company.objects.get(name='测试post公司')
        self.user.organization.company = target_company
        self.user.organization.save()

    def test_company_patch(self):
        """
        """
        response = self.client.patch(reverse('api-company'), {
            'company': {
                'website': 'https://httpbin.org/'
            }
        })

        self.assertEqual(response.data['company']['website'],
                         'https://httpbin.org/')


class CompanyOtherGETTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_organization_put2",
                                             password="456565",
                                             email="test_organization_put2@django.com")
        self.user_other = User.objects.create_user(
            username="test_organization_put_other2",
            password="456565",
            email="test_organization_put_other2@django.com")
        self.company_self = Company.objects.create(name='测试公司put3')

        self.user.organization.company = self.company_self
        self.user_other.organization.company = self.company_self
        self.user.organization.save()
        self.user_other.organization.save()

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "test_organization_put2@django.com",
                "password": "456565"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_company_other_get(self):
        response = self.client.get(reverse('api-other-get-company',
                                           kwargs={'company_name': '测试公司put3'}))
        self.assertEqual(response.data['company']['name'], '测试公司put3')


class DepartmentPOSTTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_department_post",
                                             password="456565",
                                             email="test_department_post@django.com")

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "test_department_post@django.com",
                "password": "456565"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.company_self = Company.objects.create(name='测试公司')
        self.user.organization.company = self.company_self
        self.user.organization.save()

    def test_department_post(self):
        add_user_basic_model_permissions(self.user, Department,
                                         PermissionType.add)
        self.user = get_object_or_404(User, pk=self.user.pk)

        response = self.client.post(reverse('api-new-department'),
                                    {
                                        'department': {
                                            'name': '人事部'
                                        }
                                    })

        self.assertEqual(response.data['department']['name'], '人事部')


class OrganizationPatchTestCase3(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_organization_put2",
                                             password="456565",
                                             email="test_organization_put2@django.com")
        self.user_other = User.objects.create_user(
            username="test_organization_put_other2",
            password="456565",
            email="test_organization_put_other2@django.com")
        self.company_self = Company.objects.create(name='测试公司put3')

        self.user.organization.company = self.company_self
        self.user_other.organization.company = self.company_self
        self.user.organization.save()
        self.user_other.organization.save()

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "test_organization_put2@django.com",
                "password": "456565"
            }
        })
        self.token = response.data['user']['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        add_user_basic_model_permissions(self.user, Department,
                                         PermissionType.add)
        self.user = get_object_or_404(User, pk=self.user.pk)

        response = self.client.post(reverse('api-new-department'),
                                    {
                                        'department': {
                                            'name': '技术部'
                                        }
                                    })

    def test_organization_patch_right(self):
        add_user_basic_model_permissions(self.user, Organization,
                                         PermissionType.change)

        self.user = get_object_or_404(User, pk=self.user.pk)

        response = self.client.patch(reverse('api-other-organization', kwargs={
            'username': 'test_organization_put_other2'}),
                                     {
                                         'organization': {
                                             'position': 'python研发工程师',
                                             'department': {'name': '技术部'}
                                         }
                                     })

        self.assertEqual(response.data['organization']['position'],
                         'python研发工程师')
        self.assertEqual(response.data['organization']['department']['name'],
                         '技术部')


class OrganizationInviteTestCase(APITestCase):
    """
    创建两个用户
    创建公司
    主用户是那个公司的
    给主用户增加邀请用户的权限
    主用户登录
    ----------
    主用户邀请副用户
    """

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1",
                                              password="456565",
                                              email="user1@django.com")
        self.user2 = User.objects.create_user(
            username="user2",
            password="456565",
            email="user2@django.com")

        self.company = Company.objects.create(name='测试公司')

        self.user1.organization.company = self.company
        self.user1.organization.save()

        add_user_permissions(self.user1, Organization, field_or_id='invited_by',
                             permission_type=PermissionType.change)
        self.user1 = get_object_or_404(User, pk=self.user1.pk)

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "user1@django.com",
                "password": "456565"
            }
        })

        self.token = response.data['user']['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_invite_user(self):
        response = self.client.patch(
            reverse('api-invite-user', kwargs={'username': 'user2'}))

        self.assertEqual(response.data['organization']['info'], 'ok')

        # 确认被邀请用户的组织信息字段已正确填写
        user2 = User.objects.get(username='user2')

        self.assertEqual(user2.organization.invited_by, '测试公司')


class OrganizationAcceptInviteTestCase(APITestCase):
    """
    创建两个用户
    创建公司
    主用户是那个公司的
    副用户被邀请所以字段被填写
    副用户登录
    -------------
    副用户接受邀请
    """

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1",
                                              password="456565",
                                              email="user1@django.com")
        self.user2 = User.objects.create_user(
            username="user2",
            password="456565",
            email="user2@django.com")

        self.company = Company.objects.create(name='测试公司')

        self.user1.organization.company = self.company
        self.user1.organization.save()

        self.user2.organization.invited_by = '测试公司'
        self.user2.organization.save()

        response = self.client.post(reverse('api-login'), {
            "user": {
                "email": "user2@django.com",
                "password": "456565"
            }
        })

        self.token = response.data['user']['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_invite_user(self):
        response = self.client.patch(
            reverse('api-accept-invite', kwargs={'company_name': '测试公司'}))

        self.assertEqual(response.data['organization']['info'], 'ok')

        # 确认被邀请用户的公司信息
        user2 = User.objects.get(username='user2')

        self.assertEqual(user2.organization.company.name, '测试公司')
