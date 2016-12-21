# coding:utf8
# @author:nick
# @company:joyme
from django.db import models
from public_model import PublicAccount


class MaterialListModel(models.Model):
    # 素材列表
    type_choice = [('image', u'图片'), ('video', u'视频'), ('voice', u'语音'), ('news', u'图文')]
    public = models.ForeignKey(PublicAccount)
    type = models.CharField(max_length=10, choices=type_choice, verbose_name=u'素材类型')


class MediaModel(models.Model):
    # Media id列表
    public = models.ForeignKey(PublicAccount, verbose_name=u'公众号')
    type = models.CharField(max_length=10, choices=MaterialListModel.type_choice[:-1], verbose_name=u'素材管理')
    name = models.CharField(max_length=50, verbose_name=u'素材名称')
    file = models.FileField(verbose_name=u'文件', upload_to='upload')
    media_id = models.CharField(max_length=255, verbose_name=u'media_id')
    description = models.TextField(verbose_name=u'简介', help_text=u'仅上传视频素材需要填写', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u'素材模型'
        unique_together = (('type', 'name'),)


class MaterialModel(models.Model):
    public = MaterialListModel.public
    type = MaterialListModel.type
    media_id = models.CharField(max_length=255, verbose_name=u'media_id', null=True, blank=True)
    thumb_media_id = models.CharField(max_length=255, verbose_name=u'缩略图id')
