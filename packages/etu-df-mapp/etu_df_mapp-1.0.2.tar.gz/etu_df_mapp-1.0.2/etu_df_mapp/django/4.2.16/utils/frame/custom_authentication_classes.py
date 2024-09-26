# -*- coding: utf-8 -*-
# @Time    : 2024/9/20 16:32
# @Author  : Jieay
# @File    : custom_authentication_classes.py

import logging

logger = logging.getLogger(__name__)

from rest_framework.authentication import TokenAuthentication, exceptions, HTTP_HEADER_ENCODING
from django.utils.translation import gettext_lazy as _
from utils.comm.commapi import get_base64_decode


def get_xat_header(request):
    """
    Return request's 'Xat:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    # 获取自定义请求头
    auth = request.META.get('HTTP_XAT', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class WebTokenAuthentication(TokenAuthentication):

    keyword = 'Skey'

    def authenticate(self, request):
        # 从请求头部，header 获取字段
        # [b'Skey', b'ZThhNjNjZDk0Y2YyMzNlM2U5ZTI0NzZmODZmMzY3YWY5ZWI0OGNhNA==']
        auth = get_xat_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            # header获取字段值是字节码（bytes），这里解码需要使用字节码，所以直接取值就可以
            # 字节码转字符串可以使用 auth[1].decode()
            token = get_base64_decode(auth[1])
        except Exception:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token
