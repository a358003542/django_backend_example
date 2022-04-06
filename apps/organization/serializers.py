#!/usr/bin/env python
# -*-coding:utf-8-*-

from rest_framework import serializers

from .models import Organization, Company, Department, Role


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'address', 'website')

    def update(self, instance, validated_data):
        need_update_attr = ['address', 'website']

        for attr_name in need_update_attr:
            attr = validated_data.pop(attr_name, None)
            if attr is not None:
                setattr(instance, attr_name, attr)

        instance.save()
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    parent_department_name = serializers.CharField(source='parent.name',
                                                   default="")

    class Meta:
        model = Department
        fields = ('name', 'company', 'parent_department_name')
        read_only_fields = ('parent_department_name',)

    def create(self, validated_data):
        """
        新增记录
        """
        department_name = validated_data['name']
        company_name = self.context.get('company_name')
        company = Company.objects.get(name=company_name)
        department = Department.objects.create(company=company,
                                               name=department_name)
        return department


class RoleSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Role
        fields = ('name', 'company')

    def create(self, validated_data):
        """
        新增角色
        """
        name = validated_data['name']
        company_name = self.context.get('company_name')
        company = Company.objects.get(name=company_name)
        role = Role.objects.create(company=company,
                                        name=name)
        return role

class OrganizationSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    department = DepartmentSerializer()

    class Meta:
        model = Organization
        fields = ('user', 'company', 'department', 'position')

    def update(self, instance, validated_data):
        position = validated_data.pop('position', '')
        department = validated_data.pop('department', '')

        changed = False

        if position:
            changed = True
            instance.position = position

        if department:
            changed = True
            target_department = Department.objects.get(company=instance.company,
                                                       name=department['name'])
            if target_department:
                instance.department = target_department
            else:
                raise Exception('Department with this department name does not exists.')

        if changed:
            instance.save()

        return instance
