# coding:utf8
# @author:nick
# @company:joyme

from django.db import models
from django.contrib.auth.models import User


class LogModel(models.Model):
    # 日志表
    user = models.ForeignKey(User, verbose_name=u'用户')
    path = models.CharField(max_length=255, verbose_name=u'路径')
    request = models.TextField(verbose_name=u'请求')
    request_time = models.DateTimeField(auto_now_add=True)
