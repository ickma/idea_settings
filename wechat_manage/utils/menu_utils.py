# coding:utf8
# @author:nick
# @company:joyme
from wechat_manage.models.public_model import PublicMenuConfig
import json


def menu_info_format(menu_instance):
    """
    格式化菜单
    将生成的菜单格式化为符合官方要求的格式
    :type menu_instance:PublicMenuConfig
    :param menu_instance: 菜单Model实例
    :return:
    :rtype:PublicMenuConfig
    """
    if menu_instance.menu_type == 'view':
        menu_instance.info = json.dumps({'url': menu_instance.info})
    # todo 格式化功能选择

    if not isinstance(menu_instance.parent_index, int):
        menu_instance.parent_index = PublicMenuConfig.objects.get(public=menu_instance.public,
                                                                  menu_name=menu_instance.parent_index,
                                                                  menu_level=1).parent_index

    return menu_instance
