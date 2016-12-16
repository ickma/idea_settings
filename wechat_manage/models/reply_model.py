# coding:utf8
# @author:nick
# @company:joyme
from django.db import models
from .public_model import PublicAccount


class ReplyConfigModel(models.Model):
    # 公众号回复设置模型
    content_type_choices = [(1, u'文本'), (2, u'图片'), (3, u'语音'), (4, u'图文素材'), (5, u'视频')]
    reply_type_choices = [(1, u'关注回复'), (2, u'默认回复'), (3, u'关键字回复')]
    public = models.ForeignKey(PublicAccount, verbose_name=u'公众号')
    name = models.CharField(verbose_name=u'名称', max_length=255, null=True, blank=True)
    content_type = models.IntegerField(verbose_name=u'回复类型', choices=content_type_choices)
    reply_type = models.IntegerField(verbose_name=u'回复类型', choices=reply_type_choices)
    content = models.TextField(verbose_name=u'回复内容', null=True, blank=True)
    file = models.FileField(verbose_name=u'回复文件', blank=True, null=True)
    keywords = models.TextField(verbose_name=u'关键字', blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u'公众号回复设置'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.reply_type == 3 and not self.keywords:
            raise ValueError(u'关键字不能为空')
        if bool(self.content) == bool(self.file):
            raise ValueError(u'回复内容未选择或正确')
        super(ReplyConfigModel, self).save(force_insert, force_update, using, update_fields)
