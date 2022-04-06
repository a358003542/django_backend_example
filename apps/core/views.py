#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
import errno
import logging
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from .renderers import UploadJSONRenderer

logger = logging.getLogger(__name__)

def mkdirs(path, mode=0o777):
    """
    Recursive directory creation function base on os.makedirs
    with a little error handling.
    """
    try:
        os.makedirs(path, mode=mode)
    except OSError as e:
        if e.errno != errno.EEXIST:  # File exists
            logger.error('file exists: {0}'.format(e))


class FileUploadAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [FileUploadParser]
    renderer_classes = (UploadJSONRenderer,)

    def put(self, request, filename):
        """
        wb+ put 文件新建或者替换模式
        """
        username = request.user.username
        file_obj = request.data['file']
        abs_filename = os.path.join(settings.MEDIA_ROOT, username, filename)

        url_path = [p for p in settings.MEDIA_URL.split('/') if p]
        url_path += [username, filename]
        target_file_url  = '/'.join(url_path)

        # make sure folder exists
        mkdirs(os.path.dirname(abs_filename))

        with open(abs_filename, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        data = {
            'file_url': target_file_url,
        }

        return Response(data, status=204)



class ImageUploadAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [FileUploadParser]
    renderer_classes = (UploadJSONRenderer,)

    def put(self, request, filename):
        username = request.user.username
        file_obj = request.data['file']
        abs_filename = os.path.join(settings.MEDIA_ROOT, username, filename)

        url_path = [p for p in settings.MEDIA_URL.split('/') if p]
        url_path += [username, filename]
        target_file_url  = '/'.join(url_path)

        mkdirs(os.path.dirname(abs_filename))

        with open(abs_filename, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        data = {
            'file_url': target_file_url,
        }

        return Response(data, status=204)