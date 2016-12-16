# coding:utf8
# @author:nick
# @company:joyme
from django.db import models
from django.contrib.auth.models import User


class FileUpload(models.Model):
    # 文件上传 
    file_path = models.FilePathField(verbose_name=u'文件路径')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'上传时间')
    file_size = models.FloatField(verbose_name=u'文件大小 ')
    user = models.ForeignKey(User, verbose_name=u'上传用户')
    file_hash = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']
        verbose_name_plural = verbose_name = u'文件上传'
