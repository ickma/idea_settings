# coding:utf8
# @author:nick
# @company:joyme
from app.models.feather_models import FeatureModel
from .menu_form import BaseForm
from django import forms
from wechat_manage.models.reply_model import ReplyConfigModel
from app.models.feather_models import FeatureModel


class BaseReplyForm(BaseForm):
    # 设置关注欢迎语
    content_type_choices = ReplyConfigModel.content_type_choices
    content_type = forms.IntegerField(widget=forms.Select(choices=content_type_choices), label=u'选择回复类型')
    reply_content = forms.CharField(widget=forms.Textarea, label=u'添加回复语', required=False)
    # todo 实现素材的自动选择
    # matiarial=forms.IntegerField(widget=)
    file = forms.FileField(label=u'上传文件', required=False)


class DefaultReplyForm(BaseReplyForm):
    # 设置默认回复
    pass


class KeyWorldReplyForm(BaseReplyForm):
    # 设置关键字回复
    name = forms.CharField(label=u'名称')
    keywords = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'多个关键字请单独另起一行'}), label=u'关键字')
    # 选择功能
    feather = forms.CharField(widget=forms.Select(choices=FeatureModel.get_choices()), required=False, label=u'选择功能')
