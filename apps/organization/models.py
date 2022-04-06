from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimestampedModel


class Company(TimestampedModel):
    """
    注册到应用中公司信息和可用部门名字清单和可用职位名字清单
    """
    name = models.CharField('name', max_length=255, help_text='公司名字',
                            unique=True)

    address = models.CharField('address', max_length=500, blank=True,
                               default="", help_text='公司地址')
    website = models.URLField('website', blank=True, null=True)

    class Meta:
        db_table = 'company'

    def __str__(self):
        return self.name


class SubCompany(TimestampedModel):
    """
    分公司 一个公司可以有多个分公司
    """
    name = models.CharField('name', max_length=255, help_text='分公司名字')

    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name='sub_companys')

    def __str__(self):
        return self.name

class Department(TimestampedModel):
    """
    某个公司内部的部门
    """
    company = models.ForeignKey('organization.Company',
                                on_delete=models.CASCADE, blank=True)

    name = models.CharField('name', max_length=255, help_text='部门名字')

    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name='children',
                               on_delete=models.CASCADE)

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.name

class Role(TimestampedModel):
    """
    角色 公司内用户扮演的角色
    """
    name = models.CharField(_('name'), max_length=150, unique=True)

    company = models.ForeignKey('organization.Company',
                                on_delete=models.CASCADE, null=True, blank=True)

    group = models.OneToOneField('auth.Group', on_delete=models.CASCADE,
                                 null=True, blank=True)

    category = models.ForeignKey('organization.RoleCategory',
                                 on_delete=models.CASCADE, null=True,
                                 blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        permissions = [
            ("change_role_permission", "Can change role permission"),
        ]


class RoleCategory(TimestampedModel):
    """
    角色组
    """
    name = models.CharField(_('name'), max_length=150, unique=True)

    class Meta:
        db_table = 'role_category'

    def __str__(self):
        return self.name

class Organization(TimestampedModel):
    """
    用户的组织信息
    """
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)

    company = models.ForeignKey('organization.Company',
                                on_delete=models.CASCADE,
                                related_name='company_users', null=True,
                                blank=True)

    # 一个用户只能在一个部门
    department = models.ForeignKey('organization.Department',
                                   on_delete=models.CASCADE,
                                   related_name='department_users', null=True,
                                   blank=True)

    # 用户在公司所扮演的角色 和权限控制相关
    roles = models.ManyToManyField(Role, verbose_name=_('roles'), blank=True,
                                   related_name="user_set")

    position = models.CharField('position', max_length=255, help_text='用户的职位',
                                null=True, blank=True)

    # 被那个公司邀请 用户接受邀请的时候该字段不能为空并且公司名相同才能正式接受邀请
    invited_by = models.CharField('invited_by', max_length=255,
                                  help_text='被那个公司邀请')

    class Meta:
        db_table = 'auth_user_organization'
        permissions = [
            ("change_organization_invited_by", "Can invite people to company"),
            ("change_organization_roles", "Change user in organization roles")
        ]

    def __str__(self):
        return self.user.username
