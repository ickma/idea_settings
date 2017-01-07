# coding:utf8
# @author:nick
# @company:joyme
from django.db import models


class Media(models.Model):
    media_id = models.CharField(verbose_name=u'素材ID', max_length=255)
    media_download_path = models.CharField(verbose_name=u'素材下载地址', max_length=255)
