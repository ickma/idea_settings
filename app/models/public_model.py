# coding:utf8
# @author:nick
# @company:joyme
# 公众号相关model
from django.db import models


class PublicAccount(models.Model):
    encrypt_mode_choices = (('normal', u'明文模式'), ('compatible', u'兼容模式'), ('safe', u'安全模式'))
    public_name = models.CharField(max_length=255, verbose_name=u'公众号名称')
    token = models.CharField(max_length=255, verbose_name=u'公众号token')
    app_id = models.CharField(max_length=255, verbose_name=u'公众号id', unique=True)
    app_secret = models.CharField(max_length=255, verbose_name=u'公众号secret')
    encrypt_mode = models.CharField(max_length=255, choices=encrypt_mode_choices, verbose_name=u'消息加解密方式')
    encrypt_aes_key = models.CharField(max_length=255, verbose_name=u'公众平台开发者选项中的 EncodingAESKey', null=True)
    access_token = models.CharField(max_length=255, verbose_name=u'公众号access token')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'公众号创建时间', editable=False)
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'信息更新时间', editable=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        自定义save 方法
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        if self.encrypt_mode != 'normal' and self.encrypt_aes_key == '':
            raise Exception(u'没有输入正确的EncodingAESKey')
        super(PublicAccount, self).save(force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return self.public_name

    class Meta:
        verbose_name = u'公众号配置'
