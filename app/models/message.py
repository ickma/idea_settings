# coding:utf8
# @author:nick
# @company:joyme

from django.db import models
from wechat_manage.models.followers_model import PublicFollowers
from wechat_manage.models.public_model import PublicAccount
from wechat_manage.models.reply_model import ReplyConfigModel
from feather_models import FeatureModel
from wechat_sdk.messages import WechatMessage


class MsgResponse(models.Model):
    # msg = models.ForeignKey(Message)
    response_type = models.CharField(max_length=255, verbose_name=u'回复类型',
                                     choices=ReplyConfigModel.content_type_choices)
    public = models.ForeignKey(PublicAccount, verbose_name=u'公众号')
    content = models.TextField(verbose_name=u'回复文本内容', null=True)
    msgid = models.CharField(verbose_name=u'回复的msgid', null=True, max_length=255)
    feather = models.ForeignKey(FeatureModel, verbose_name=u'触发的事件', null=True)
    keywords = models.CharField(verbose_name=u'触发的关键字', null=True, max_length=255)


class Message(models.Model):
    type_choices = [('image', u'图片'), ('text', u'文本'), ('voice', u'语音'), ('video', u'视频'), ('shortvideo', u'小视频'),
                    ('link', u'链接'), ('location', u'地理位置')]
    form_user = models.ForeignKey(PublicFollowers, verbose_name=u'用户')
    public = models.ForeignKey(PublicAccount, verbose_name=u'公众号')
    type = models.CharField(choices=type_choices, verbose_name=u'消息类型', max_length=20)
    content = models.TextField(verbose_name=u'消息内容', null=True)
    msgid = models.BigIntegerField(verbose_name=u'消息ID', unique=True)
    create_time = models.IntegerField(verbose_name=u'创建时间')
    picurl = models.CharField(max_length=255, verbose_name=u'图片链接', null=True)
    mediaid = models.CharField(max_length=255, verbose_name=u'mediaID', null=True)
    format = models.CharField(max_length=20, verbose_name=u'文件格式', null=True)
    thum_mediaid = models.CharField(max_length=255, verbose_name=u'缩略图mediaID', null=True)
    location_x = models.FloatField(verbose_name=u'纬度', null=True)
    location_y = models.FloatField(verbose_name=u'精度', null=True)
    scale = models.IntegerField(verbose_name=u'地图缩放大小', null=True)
    label = models.TextField(verbose_name=u'地理位置', null=True)
    url = models.TextField(verbose_name=u'链接', null=True)
    description = models.TextField(verbose_name=u'简介', null=True)
    title = models.TextField(verbose_name=u'标题', null=True)
    response = models.OneToOneField(MsgResponse, verbose_name=u'回复内容', null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # todo 实现消息处理和save逻辑
        msg_instance = self.msg_instance
        if msg_instance.type == 'text':

        super(Message, self).save(force_insert, force_update, using, update_fields)

    @property
    def msg_instance(self):
        return self._msg_instance

    @msg_instance.setter
    def msg_instance(self, value):
        if isinstance(value, WechatMessage):
            self._msg_instance = value
