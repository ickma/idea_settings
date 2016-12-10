# coding:utf8
# @author:nick
# @company:joyme

from django import forms
from wechat_manage.models.public_model import PublicMenuConfig


class MenuCreate(forms.Form):
    # 公众号菜单创建
    menu_cates = PublicMenuConfig.menu_cats
    menu_name = forms.CharField(max_length=25, label=u'菜单名单')
    menu_level = forms.IntegerField(widget=forms.Select(choices=[(1, u'1级菜单'), (2, u'2级菜单')]), label=u'菜单级别')
    menu_cates = forms.CharField(widget=forms.Select(choices=menu_cates), label=u'菜单类型')
