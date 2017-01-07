# coding:utf8
# @author:nick
# @company:joyme

from django.db import models
from wechat_manage.models.followers_model import PublicFollowers
from wechat_manage.models.public_model import PublicAccount
from wechat_manage.models.reply_model import ReplyConfigModel
from feather_models import FeatureModel
from media import Media
from wechat_sdk.messages import WechatMessage, EventMessage, ImageMessage, LinkMessage, TextMessage, VideoMessage \
    , VoiceMessage, ShortVideoMessage, LocationMessage, UnknownMessage
from wechat_sdk import WechatBasic


class MsgResponse(models.Model):
    # msg = models.ForeignKey(Message)
    response_type = models.CharField(max_length=255, verbose_name=u'回复类型',
                                     choices=ReplyConfigModel.content_type_choices)
    public = models.ForeignKey(PublicAccount, verbose_name=u'公众号')
    content = models.TextField(verbose_name=u'回复文本内容', null=True)
    msgid = models.CharField(verbose_name=u'回复的msgid', null=True, max_length=255)
    feather = models.ForeignKey(FeatureModel, verbose_name=u'触发的事件', null=True)
    keywords = models.CharField(verbose_name=u'触发的关键字', null=True, max_length=255)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now=True)


class Message(models.Model):
    type_choices = [('image', u'图片'), ('text', u'文本'), ('voice', u'语音'), ('video', u'视频'), ('shortvideo', u'小视频'),
                    ('link', u'链接'), ('location', u'地理位置'), ('click', u'菜单'), ('view', u'菜单')]
    form_user = models.ForeignKey(PublicFollowers, verbose_name=u'用户')
    public = models.ForeignKey(PublicAccount, verbose_name=u'公众号')
    xml = models.TextField(verbose_name=u'原始xml')
    type = models.CharField(choices=type_choices, verbose_name=u'消息类型', max_length=20)
    content = models.TextField(verbose_name=u'消息内容', null=True)
    msgid = models.BigIntegerField(verbose_name=u'消息ID', null=True)
    create_time = models.IntegerField(verbose_name=u'创建时间戳')
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
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
    event_type = models.CharField(max_length=20, null=True, verbose_name=u'事件类型')
    event_key = models.CharField(max_length=50, null=True, verbose_name=u'事件key')
    ticket = models.TextField(verbose_name=u'二维码换取ticket')
    latitude = models.FloatField(verbose_name=u'上报的地理位置的纬度', null=True)
    longitude = models.FloatField(verbose_name=u'上报的地理位置的经度', null=True)
    precision = models.FloatField(verbose_name=u'上报的地理位置的静度', null=True)
    media = models.ForeignKey(Media, verbose_name=u'素材', null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, wechatsdk=None):
        """
        :type wechatsdk:WechatBasic
        :param force_insert: 
        :param force_update: 
        :param using: 
        :param update_fields: 
        :param wechatsdk: 
        :return: 
        """
        msg_instance = self.msg_instance
        """:type :TextMessage|LocationMessage|ImageMessage|VoiceMessage|EventMessage|LinkMessage|VideoMessage|ShortVideoMessage"""
        self.type = msg_instance.type
        self.create_time = msg_instance.time
        self.msgid = msg_instance.id
        if hasattr(msg_instance, 'content'):
            self.content = msg_instance.content
        # 自动下载用户上传的媒体文件，声音,视频等
        if hasattr(msg_instance, 'media_id'):
            self.mediaid = msg_instance.media_id
            response = wechatsdk.download_media(media_id=self.media)
            from django.conf import settings
            import os
            with open(os.path.join(settings.BASE_DIR, 'download', self.mediaid), 'wb') as f:
                f.write(response)
            media_instance = Media(media_id=self.media, media_download_path=os.path.join('download', self.mediaid))
            self.media = media_instance

        if hasattr(msg_instance, 'picurl'):
            self.picurl = msg_instance.picurl
        if hasattr(msg_instance, 'format'):
            self.format = msg_instance.format
        if hasattr(msg_instance, 'thumb_media_id'):
            self.thum_mediaid = msg_instance.thumb_media_id
        if hasattr(msg_instance, 'location'):
            self.location_x = msg_instance.location[0]
            self.location_y = msg_instance.location[1]
        if hasattr(msg_instance, 'scale'):
            self.scale = msg_instance.scale
        if hasattr(msg_instance, 'label'):
            self.label = msg_instance.label
        if hasattr(msg_instance, 'url'):
            self.url = msg_instance.url
        if hasattr(msg_instance, 'description'):
            self.description = msg_instance.description
        if hasattr(msg_instance, 'title'):
            self.title = msg_instance.title
        if hasattr(msg_instance, 'key'):
            self.event_key = msg_instance.key

        if hasattr(msg_instance, 'latitude'):
            self.latitude = msg_instance.latitude
            self.longitude = msg_instance.longitude
            self.precision = msg_instance.precision

        # todo  检查当前msgid  是否存在重复
        super(Message, self).save(force_insert, force_update, using, update_fields)

    @property
    def msg_instance(self):
        return self._msg_instance

    @msg_instance.setter
    def msg_instance(self, value):
        if isinstance(value, WechatMessage):
            self._msg_instance = value
        else:
            raise TypeError(u'不是合法的WechatMessage实例')

    @classmethod
    def group_messages(cls):
        return cls.objects.raw('SELECT * FROM app_message GROUP BY form_user_id')

    def display(self):
        if self.content:
            return self.content
        elif self.picurl:
            return '<a href="{0}"><img src="{0}" style="height:30px;width:auto"></a>'.format(self.picurl)
        if self.event_key:
            try:
                return u'点击菜单:%s' % self.response.feather
            except AttributeError, FeatureModel.DoesNotExist:
                return ''
        if self.type == 'voice':
            return """
            <audio controls="controls">
  <source src="{0}" type="audio/ogg">
Your browser does not support the audio element.
</audio>

            """.format(self.media.media_download_path)
        if self.url:
            return u'点击菜单:浏览%s' % self.url

    class Meta:
        ordering = ['-id']
