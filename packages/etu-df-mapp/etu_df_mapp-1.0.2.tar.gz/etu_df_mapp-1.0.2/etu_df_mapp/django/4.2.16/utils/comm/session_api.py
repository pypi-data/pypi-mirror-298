# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 16:13
# @Author  : Jieay
# @File    : session_api.py

import logging

from django.conf import settings
from utils.comm.commapi import get_base64_encoded


logger = logging.getLogger(__name__)


def get_session_key_expire():
    """
    获取 session_key 过期时间，单位秒
    Returns: `int`
    """
    try:
        session_key_expire = settings.COOKIE_SESSION_KEY_EXPIRE_MINUTES * 60
    except Exception as e:
        logger.error(e)
        session_key_expire = 60 * 60 * 24 * 30  # 2592000 秒
    return session_key_expire


def set_response_session_key(response, token, msg=''):
    """
    构造返回数据，设置 cookie 信息，添加 session_key 字段
    Args:
        response: `response` 返回实例
        token: `str` Token
        msg: `str` 信息

    Returns: `response` 返回实例
    """
    sk_expire = get_session_key_expire()
    session_key = get_base64_encoded(token)
    response.set_cookie(key='session_key', value=session_key, max_age=sk_expire, expires=sk_expire)
    logger.debug(f'{msg}, session_key: {session_key}')
    return response
