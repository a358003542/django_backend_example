#!/usr/bin/env python
# -*-coding:utf-8-*-

from django.urls import path

from .views import FileUploadAPIView, ImageUploadAPIView

urlpatterns = [
    path('api/upload-image/<filename>/', ImageUploadAPIView.as_view(),
         name='api-upload-image'),
    path('api/upload-file/<filename>/', FileUploadAPIView.as_view(),
         name='api-upload-file'),
]
