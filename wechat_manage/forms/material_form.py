# coding:utf8
# @author:nick
# @company:joyme

from django.forms import ModelForm
from django import forms
from wechat_manage.models import material_model
from menu_form import BaseForm


class MaterialMediaForm(ModelForm):
    # 素材生成表
    class Meta:
        model = material_model.MediaModel
        fields = ['type', 'name','file', 'description']
