# coding:utf8
# @author:nick
# @company:joyme
from . import register
from wechat_manage.models.public_model import PublicMenuConfig
import json


@register.filter(name='get_menu_parent')
def get_menu_parent_name(menu_id):
    """
    获取当前菜单的父级菜单
    :param menu_id:
    :return:
    """
    menu_instance = PublicMenuConfig.objects.get(id=menu_id)
    if menu_instance.menu_level == 1:
        return ''
    else:
        return PublicMenuConfig.objects.get(parent_index=menu_instance.parent_index, menu_level=1).menu_name


@register.filter(name='format_menu_info')
def format_menu_info(info):
    """
    对当前菜单的绑定时间进行格式化
    :param info:
    :return:
    """
    info = json.loads(info)
    menu_type = info.get('type', None)
    if not menu_type:
        return ''
    if menu_type == 'click':
        return info['key']
    elif menu_type == 'view':
        return info['url']
