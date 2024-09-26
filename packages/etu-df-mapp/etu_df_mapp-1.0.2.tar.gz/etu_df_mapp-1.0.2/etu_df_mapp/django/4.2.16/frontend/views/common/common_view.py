# -*- coding: utf-8 -*-
# @Time    : 2024/9/14 17:05
# @Author  : Jieay
# @File    : common_view.py
import json
import logging

logger = logging.getLogger(__name__)

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.templatetags.static import static as templatetags_static
from django.template.response import TemplateResponse
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from utils.frame.api_view_external import BaseOpenApiView
from drf_spectacular.utils import extend_schema
from utils.comm.gen_captcha import get_captcha as img_captcha


def login(request):
    """登录"""
    login_type = request.session.get('login-type')
    logger.info(f'登录，login_type: {login_type}')
    # 使用账户密码登录
    if login_type == 'admin':
        redirect_url = reverse('web_login')
    # 使用 CAS 登录
    elif login_type == 'cas':
        redirect_url = reverse('cas_ng_login')
    else:
        redirect_url = reverse('web_login')
    return redirect(redirect_url)


def logout(request):
    """退出"""
    login_type = request.session.get('login-type')
    logger.info(f'退出，login_type: {login_type}')
    if login_type == 'admin':
        redirect_url = reverse('web_logout')
    elif login_type == 'cas':
        redirect_url = reverse('cas_ng_logout')
    else:
        redirect_url = reverse('web_logout')
    return redirect(redirect_url)


def web_login(request):
    """前端登录页面"""
    data = {
        'frontend_name': settings.FRONTEND_NAME
    }
    return TemplateResponse(request, "login.html", context=data)


def web_logout(request):
    """前端退出"""
    request.session.pop("user", None)
    # 获取重定向URL
    redirect_url = reverse('web_login')
    auth_logout(request)
    return redirect(redirect_url)


def get_captcha_code_from_session(request):
    # 从会话中获取验证码文本
    return request.session.get("code")


class GetWebGenerateCaptchaView(BaseOpenApiView):
    """获取Web登录验证码信息"""

    @extend_schema(
        tags=['Web'],
        summary='WebGenerateCaptcha',
        description='获取Web登录验证码信息接口',
        methods=['GET'],
        responses={200: str}
    )
    def get(self, request):
        img, text = img_captcha()
        request.session['code'] = text
        request.session['frontend_name'] = settings.FRONTEND_NAME
        # https://unpkg.com/outeres@0.0.10/demo/avatar/1.jpg
        image_url = templatetags_static('images/avatar/1.jpg')
        request.session['avatar'] = image_url
        return StreamingHttpResponse(streaming_content=img, content_type='image/png')


class GetWebVerifyCaptchaView(BaseOpenApiView):
    """校验Web登录验证码信息"""

    @extend_schema(
        tags=['Web'],
        summary='WebVerifyCaptcha',
        description='校验Web登录验证码信息接口',
        methods=['GET'],
        responses={200: dict}
    )
    def get(self, request):
        data = {"msg": "Verification code correct.", "code": 200}
        captcha_code = request.GET.get('captcha_code', '')
        stored_captcha_code = get_captcha_code_from_session(request)
        if not captcha_code:
            data['msg'] = 'No verification code is entered.'
            data['code'] = 400
            return JsonResponse(data=data, safe=False)
        if not stored_captcha_code:
            data['msg'] = 'Verification code error.'
            data['code'] = 400
            return JsonResponse(data=data, safe=False)
        if captcha_code.lower() != stored_captcha_code.lower():
            data['msg'] = 'The verification code has expired.'
            data['code'] = 400
            return JsonResponse(data=data, safe=False)
        return JsonResponse(data=data, safe=False)


class GetWebApiLoginView(BaseOpenApiView):
    """Web登录API信息"""

    @extend_schema(
        tags=['Web'],
        summary='WebApiLogin',
        description='Web登录API信息接口',
        methods=['POST'],
        request=dict,
        responses={200: dict}
    )
    def post(self, request):
        data = {"msg": "登录成功", "code": 200}
        captcha = request.data.get('captcha')
        username = request.data.get('username')
        password = request.data.get('password')
        stored_captcha_code = get_captcha_code_from_session(request)
        if not stored_captcha_code:
            data['msg'] = 'Verification code error.'
            data['code'] = 400
            return JsonResponse(data=data, safe=False)
        if captcha.lower() != stored_captcha_code.lower():
            data['msg'] = 'The verification code has expired.'
            data['code'] = 400
            return JsonResponse(data=data, safe=False)
        # 验证用户信息
        user_cache = authenticate(
            request, username=username, password=password
        )
        if user_cache is None:
            data['msg'] = f'The user or password is incorrect. username: {username}'
            data['code'] = 400
            return JsonResponse(data=data, safe=False)
        elif not user_cache.is_active:
            data['msg'] = f'The user not activated. username: {username}'
            data['code'] = 400
            return JsonResponse(data=data, safe=False)
        # 通过用户认证后登录
        auth_login(request, user_cache)
        request.session['user'] = {'user': username}
        request.session['login-type'] = 'admin'
        return JsonResponse(data=data, safe=False)
