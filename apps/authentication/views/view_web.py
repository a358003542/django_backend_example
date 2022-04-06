#!/usr/bin/env python
# -*-coding:utf-8-*-

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:
    """
    首页
    """
    return TemplateResponse(
        request,
        "home.html",
        {
            "test": 'ok',
        },
    )


