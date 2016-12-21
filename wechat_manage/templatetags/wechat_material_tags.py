# coding:utf8
# @author:nick
# @company:joyme
from . import register
from wechat_manage.models.material_model import MediaModel


@register.filter(name='format_material_display')
def format_material_display(material):
    """
    :type material:MediaModel
    :param material:
    :return:
    """
    material_type = material.type
    if material_type == 'image':
        return '<div class="hover_zoom_img"><a href="%s"><img src="%s" ></a></div>' % (
            material.file.url, material.file.url)
    return material.file.path
