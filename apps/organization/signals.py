#!/usr/bin/env python
# -*-coding:utf-8-*-


from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.organization.models import Role
from django.contrib.auth.models import Group


def create_group_name_by_role(role):
    """
    根据对应的Role模型创建Group的名字
    """
    company_id = role.company_id
    assert company_id is not None
    name = f'{company_id}_{role.name}'
    return name

def group_name_to_role(group_name):
    """
    根据群组名字分析得到角色名
    """
    i = group_name.find('_')
    if i < 0:
       raise Exception('this group name is not connected to a role')
    else:
        company_id = group_name[:i]
        role_name = group_name[i+1:]
        return company_id, role_name



@receiver(post_save, sender=Role)
def create_related_group(sender, instance, created, *args, **kwargs):
    """
    Role实际起作用还是依赖于Group类，所以每新建一个Role就会自动新建一个Group类
    """
    if instance and created:
        name = create_group_name_by_role(instance)
        instance.group = Group.objects.create(name=name)
        instance.save()

