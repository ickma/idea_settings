# coding:utf8
# @author:nick
# @company:joyme
import json

from django import forms
from django.forms.utils import ErrorList

from wechat_manage.models.public_model import PublicMenuConfig
from app.models.feather_models import FeatureModel


class BaseForm(forms.Form):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None):
        super(BaseForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                       empty_permitted, field_order, use_required_attribute)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width:40%'})


class MenuCreateForm(BaseForm):
    # 公众号菜单创建form

    menu_cates_choice = PublicMenuConfig.menu_cats[:3]
    menu_name = forms.CharField(max_length=10, label=u'菜单名单')
    menu_level = forms.IntegerField(
        widget=forms.Select(choices=[(1, u'1级菜单'), (2, u'2级菜单')], attrs={'readonly': 'readonly'}),
        label=u'菜单级别')
    menu_cates = forms.CharField(widget=forms.Select(choices=menu_cates_choice), label=u'菜单类型')
    feathers = forms.CharField(label=u'选择功能', widget=forms.Select(choices=FeatureModel.get_choices()))
    url = forms.CharField(label=u'填写网址', required=False)
    parent_menu = forms.CharField(label=u'上级菜单', widget=forms.Select())

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None, public=None):
        """
        初始化方法
        在初始化时根据当前菜单选项等，对form进行若干初始化操作
        :param data:
        :param files:
        :param auto_id:
        :param prefix:
        :param initial:
        :param error_class:
        :param label_suffix:
        :param empty_permitted:
        :param field_order:
        :param use_required_attribute:
        """
        super(MenuCreateForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                             empty_permitted, field_order, use_required_attribute)
        if public:
            self.fields['parent_menu'].widget.choices = PublicMenuConfig.get_level_one_menus(public)
        if initial['menu_level'] == 1:
            self.fields['parent_menu'] = None

        if initial.get('url'):
            self.fields['menu_cates'].initial = 'view'
            self.fields['url'].initial = initial['url']
        elif initial.get('key'):
            self.fields['menu_cates'].initial = 'click'
            self.fields['feathers'].initial = initial['key']
        elif initial['menu_cates'] == 'as_parent':
            self.fields['menu_cates'].initial = 'as_parent'
