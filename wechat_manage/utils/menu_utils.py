# coding:utf8
# @author:nick
# @company:joyme
from wechat_manage.models.public_model import PublicMenuConfig
import json
from app.models.feather_models import FeatureModel


def menu_info_format(menu_instance):
    """
    格式化菜单
    将生成的菜单格式化为符合官方要求的格式
    :type menu_instance:PublicMenuConfig
    :param menu_instance: 菜单Model实例
    :return:
    :rtype:PublicMenuConfig
    """
    # todo 格式化功能选择
    # 格式化当前 菜单对应的功能
    if menu_instance.menu_type == 'click':
        menu_instance.feather.key = menu_instance.feather.feather_class

    if not isinstance(menu_instance.parent_index, (int, long)) and menu_instance.menu_level == 2:
        menu_instance.parent_index = PublicMenuConfig.objects.get(public=menu_instance.public,
                                                                  menu_name=menu_instance.parent_index,
                                                                  menu_level=1).parent_index

    return menu_instance
