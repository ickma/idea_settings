# coding:utf8
# @author:nick
# @company:joyme

from django.db import models
from django.contrib.auth.models import User


class WebRequest(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'请求时间')
    host = models.CharField(max_length=1000, verbose_name=u'域名')
    path = models.CharField(max_length=1000, verbose_name=u'端口')
    method = models.CharField(max_length=50, verbose_name=u'请求方法')
    uri = models.CharField(max_length=2000, verbose_name=u'请求路径')
    status_code = models.IntegerField(verbose_name=u'状态码')
    user_agent = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u'userAgent')
    remote_addr = models.CharField(max_length=255)
    remote_addr_fwd = models.CharField(blank=True, null=True, max_length=255)
    meta = models.TextField(verbose_name='META')
    cookies = models.TextField(blank=True, null=True)
    get = models.TextField(blank=True, null=True, verbose_name=u'get参数')
    post = models.TextField(blank=True, null=True, verbose_name=u'post参数')
    raw_post = models.TextField(blank=True, null=True)
    is_secure = models.BooleanField(verbose_name='is_secure')
    is_ajax = models.BooleanField(verbose_name='is_ajax')
    user = models.ForeignKey(User, blank=True, null=True)


class LogModel(models.Model):
    # 日志表
    user = models.ForeignKey(User, verbose_name=u'用户',null=True)
    path = models.CharField(max_length=255, verbose_name=u'路径')
    request = models.ForeignKey(WebRequest, verbose_name=u'请求')
    request_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = u'请求log日志'
