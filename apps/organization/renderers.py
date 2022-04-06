#!/usr/bin/env python
# -*-coding:utf-8-*-

from apps.core.renderers import ConduitJSONRenderer


class CompanyJsonRenderer(ConduitJSONRenderer):
    object_label = 'company'
    pagination_object_label = 'companys'
    pagination_count_label = 'companysCount'

class DepartmentJsonRenderer(ConduitJSONRenderer):
    object_label = 'department'
    pagination_object_label = 'departments'
    pagination_count_label = 'departmentsCount'

class OrganizationJSONRenderer(ConduitJSONRenderer):
    object_label = 'organization'
    pagination_object_label = 'organizations'
    pagination_count_label = 'organizationsCount'


class RuleJSONRenderer(ConduitJSONRenderer):
    object_label = 'rule'
    pagination_object_label = 'rules'
    pagination_count_label = 'rulesCount'