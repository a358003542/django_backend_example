from django.contrib import admin

from .models import Organization, Company, Department

admin.site.register(Organization)
admin.site.register(Company)
admin.site.register(Department)