# -*- coding: utf-8 -*-
# @Time    : 2024/9/14 17:10
# @Author  : Jieay
# @File    : home_view.py

import logging

logger = logging.getLogger(__name__)

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from utils.user.membersapi import get_view_request_token
from utils.comm.session_api import set_response_session_key


@login_required(login_url='/login')
def index(request):
    token = get_view_request_token(request)
    # 检查cookies是否有session_key
    session_key = request.COOKIES.get('session_key')
    if not session_key and token:
        redirect_url = reverse('home_index')
        response = redirect(redirect_url)
        return set_response_session_key(response, token, msg='登录成功')
    return TemplateResponse(request, "home/home.html", {})
