from django.contrib import admin
from apps.authentication.models import User, Profile


admin.site.register(User)
admin.site.register(Profile)
