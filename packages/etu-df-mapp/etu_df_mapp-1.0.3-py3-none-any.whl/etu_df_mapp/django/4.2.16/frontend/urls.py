#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/20 4:28 下午
# @Author  : Jieay
# @File    : urls.py

from django.urls import path
from frontend.views.common import common_view


urlpatterns = [
    path('login', common_view.web_login, name='web_login'),
    path('logout', common_view.web_logout, name='web_logout'),
    path('generate-captcha', common_view.GetWebGenerateCaptchaView.as_view(), name='generate_captcha'),
    path('verify-captcha', common_view.GetWebVerifyCaptchaView.as_view(), name='verify_captcha'),
    path('api-login', common_view.GetWebApiLoginView.as_view(), name='admin_api_login'),
]

