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
        return u'一级菜单'
    else:
        return PublicMenuConfig.objects.get(parent_index=menu_instance.parent_index, menu_level=1).menu_name


@register.filter(name='format_menu_info')
def format_menu_info(menu):
    """
    对当前菜单的绑定时间进行格式化
    :type menu:PublicMenuConfig
    :param menu:
    :return:
    """
    level = menu.menu_level
    if level == 1:
        if not (menu.url or menu.key):
            return u'弹出子菜单'
    menu_type = menu.menu_type
    if not menu_type:
        return ''
    if menu_type == 'click':
        if menu.feather:
            return u'触发功能:%s' % menu.feather.feather_class
        else:
            return menu.key
    elif menu_type == 'view':
        return u'跳转到:%s' % menu.url
