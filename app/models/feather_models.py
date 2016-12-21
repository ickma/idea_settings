# coding:utf8
# @author:nick
# @company:joyme
from django.db import models


class FeatureModel(models.Model):
    # 功能配置表
    name = models.CharField(verbose_name=u'功能名称', max_length=255, unique=True)
    feather_class = models.CharField(verbose_name=u'功能模块', max_length=255, unique=True)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True, editable=False)
    status = models.BooleanField(verbose_name=u'状态', default=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u'功能管理'

    def __unicode__(self):
        return self.name

    @classmethod
    def get_choices(cls):
        """
        生成choices 选项
        :return:
        """
        return [(x.id, x.name) for x in cls.objects.all()]
