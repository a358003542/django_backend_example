#!/usr/bin/env python
# -*-coding:utf-8-*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

INIT_GROUP_LIST = [
    'OrganizationManager',  # 可以修改应用内所有的Organization模型数据
    'CompanyOrganizationManager',  # 可以修改本公司内所有的Organization模型数据
    'DepartmentOrganizationManager',  # 可以修改本公司内本部门内所有的Organization模型数据
    'CompanyOrdinaryMember',  # 公司一般成员
    'DepartmentOrdinayMember',  # 部门一般成员
]


class Command(BaseCommand):
    help = 'init some db data'

    def handle(self, *args, **options):
        for group_name in INIT_GROUP_LIST:
            Group.objects.create(name=group_name)

        self.stdout.write(self.style.SUCCESS('Successfully init db data'))


