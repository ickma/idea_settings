# coding:utf8
# @author:nick
# @company:joyme
from django.db import models
from .public_model import PublicAccount


class PublicFollowers(models.Model):
    public = models.ForeignKey(PublicAccount)
    openid = models.CharField(max_length=255, verbose_name='openid')
    unionid = models.CharField(max_length=255, null=True, blank=True)
    sex = models.IntegerField(choices=((1, u'男'), (2, u'女'), (3, u'未知')), verbose_name=u'性别', null=True,default=3)
    nickname = models.CharField(max_length=255, verbose_name=u'用户昵称', null=True, blank=True)
    headimgurl = models.CharField(max_length=255, verbose_name=u'用户头像', null=True, blank=True)
    country = models.CharField(verbose_name=u'国家', max_length=50, null=True)
    province = models.CharField(verbose_name=u'省份', max_length=20, null=True)
    city = models.CharField(verbose_name=u'城市', max_length=50, null=True)
    subscribe_time = models.IntegerField(verbose_name=u'关注时间', null=True)
    subscribe = models.IntegerField(choices=((1, u'已关注'), (2, u'未关注')), verbose_name=u'是否关注', null=True)
    remark = models.CharField(verbose_name='', null=True, blank=True, max_length=255)
    groupid = models.IntegerField(verbose_name=u'分组', default=0)
    language = models.CharField(max_length=20, verbose_name=u'语言', default='zh_CN')

    class Meta:
        verbose_name = verbose_name_plural = u'粉丝表'
        ordering = ['-id']
