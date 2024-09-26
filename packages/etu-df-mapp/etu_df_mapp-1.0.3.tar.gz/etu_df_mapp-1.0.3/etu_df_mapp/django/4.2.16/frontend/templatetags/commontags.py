# -*- coding: utf-8 -*-

import os
import django
from django import template
from django.db import models
from django.urls import reverse
from django.utils.functional import Promise
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag(takes_context=True)
def context_test(context):
    print(context)
    pass


@register.filter
def has_filter(spec):
    return hasattr(spec, 'parameter_name')


@register.filter
def get_date_type(spec):
    field = spec.field
    field_type = ''
    if isinstance(field, models.DateTimeField):
        field_type = 'datetime'
    elif isinstance(field, models.DateField):
        field_type = 'date'
    elif isinstance(field, models.TimeField):
        field_type = 'time'

    return field_type


@register.filter
def test(obj):
    print(obj)
    # pass
    return ''


@register.filter
def to_str(obj):
    return str(obj)


def __get_config(name):
    from django.conf import settings
    value = os.environ.get(name, getattr(settings, name, None))
    return value


@register.simple_tag
def get_setting(name):
    """
    获取设置项，默认为None
    自2022.1版本开始增加该方法
    """
    return __get_config(name)


@register.filter
def get_config(key):
    return __get_config(key)


@register.filter
def get_value(value):
    return value


def has_permission_in_config(config):
    """
    Recursively check if any menu or sub-menu in the configuration is configured with permissions.
    """
    if 'menus' in config:
        for menu in config['menus']:
            if has_permission_in_config(menu):
                return True
    if 'models' in config:
        for model in config['models']:
            if has_permission_in_config(model):
                return True
    if 'permission' in config:
        return True
    return


def get_filtered_menus(menus, user_permissions):
    def filter_menu(menu, permissions):
        if 'models' in menu:
            menu['models'] = [sub_menu for sub_menu in menu['models'] if 'permission' not in sub_menu or
                              sub_menu['permission'] in permissions]
            for sub_menu in menu['models']:
                filter_menu(sub_menu, permissions)

    menu_configs = [menu for menu in menus if 'permission' not in menu or menu['permission'] in user_permissions]
    for menu in menu_configs:
        filter_menu(menu, user_permissions)
    return menu_configs


def handler_eid(data, eid):
    for i in data:
        eid += 1
        i['eid'] = eid
        if 'models' in i:
            eid = handler_eid(i.get('models'), eid)
    return eid


@register.simple_tag(takes_context=True)
def context_to_json(context):
    json_str = '{}'

    return mark_safe(json_str)


@register.simple_tag()
def get_language():
    from django.conf import settings
    return settings.LANGUAGE_CODE.lower()


@register.filter
def get_language_code(val):
    from django.conf import settings
    return settings.LANGUAGE_CODE.lower()


def get_analysis_config():
    val = __get_config('SIMPLEUI_ANALYSIS')
    if val:
        return True
    return False


from django.db.models.fields.related import ForeignKey


def get_model_fields(model, base=None):
    field_list = []
    fields = model._meta.fields
    for f in fields:
        label = f.name
        if hasattr(f, 'verbose_name'):
            label = getattr(f, 'verbose_name')

        if isinstance(label, Promise):
            label = str(label)

        if base:
            field_list.append(('{}__{}'.format(base, f.name), label))
        else:
            field_list.append((f.name, label))

    return field_list


@register.simple_tag(takes_context=True)
def search_placeholder(context):
    cl = context.get('cl')

    # 取消递归，只获取2级
    fields = get_model_fields(cl.model)

    for f in cl.model._meta.fields:
        if isinstance(f, ForeignKey):
            fields.extend(get_model_fields(f.related_model, f.name))

    verboses = []

    for s in cl.search_fields:
        for f in fields:
            if f[0] == s:
                verboses.append(f[1])
                break

    return ",".join(verboses)


@register.simple_tag
def get_tz_suffix():
    # 判断settings.py中的TZ是否为false
    tz = __get_config('USE_TZ')
    # 必须明确指定为True的时候，才返回+8 的后缀
    if tz:
        return '+08:00'
    return ''


def get_current_app(request):
    app = None
    if hasattr(request, 'current_app'):
        app = getattr(request, 'current_app')
    elif hasattr(request, 'model_admin'):
        model_admin = getattr(request, 'model_admin')
        if hasattr(model_admin, 'opts'):
            opts = getattr(model_admin, 'opts')
            app = opts.app_config.name
    return app


@register.simple_tag(takes_context=True)
def get_model_ajax_url(context):
    opts = context.get("opts")
    key = "admin:{}_{}_ajax".format(opts.app_label, opts.model_name)
    try:
        return reverse(key)
    except:
        pass


@register.simple_tag
def has_enable_admindoc():
    from django.conf import settings
    apps = settings.INSTALLED_APPS
    return 'django.contrib.admindocs' in apps


@register.simple_tag(takes_context=True)
def has_admindoc_page(context):
    if hasattr(context, 'template_name'):
        return context.template_name.find('admin_doc') == 0
    return False


@register.simple_tag
def get_boolean_choices():
    return (
        ('True', _('Yes')),
        ('False', _('No'))
    )


@register.simple_tag
def django_version_is_gte_32x():
    arrays = django.get_version().split(".")
    version = []
    for s in arrays:
        version.append(int(s))
    return tuple(version) >= (3, 2)
