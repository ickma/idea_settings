# coding:utf8
# @author:nick
# @company:joyme
from django.db import models
from django.contrib.auth.models import User


# from wechat_manage.models.followers_model import PublicFollowers


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


class PresentSendActivity(models.Model):
    from wechat_manage.models.public_model import PublicAccount
    """礼包发放活动管理"""
    public = models.ForeignKey(verbose_name=u'公众号', to=PublicAccount)
    name = models.CharField(verbose_name=u'活动名称', max_length=100, unique=True)
    start_date = models.DateTimeField(verbose_name=u'开始时间')
    end_date = models.DateTimeField(verbose_name=u'结束时间', null=True)
    create_user = models.ForeignKey(User, verbose_name=u'创建人')
    create_time = models.DateTimeField(auto_now_add=True)
    # total_per_day = models.IntegerField(verbose_name=u'每天最多发放量', null=True)
    # total_per_day_per_follower = models.IntegerField(verbose_name=u'每人每天最多发放量', default=1)
    # total_per_follower = models.IntegerField(verbose_name=u'每个用户累计最多领取量', default=1)
    status = models.BooleanField(verbose_name=u'状态', default=True)
    not_start_prompt=models.CharField(max_length=255,verbose_name=u'未开始提示语')
    end_prompt = models.CharField(max_length=255, verbose_name=u'结束提示语')
    exceed_prompt = models.CharField(max_length=255, verbose_name=u'奖品发放完毕提示语')
    duplicate_prompt = models.CharField(max_length=255, verbose_name=u'重复领取提示语')

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = '礼包发放活动'

    def __unicode__(self):
        return self.name


class Present(models.Model):
    """礼包模型"""
    from wechat_manage.models.followers_model import PublicFollowers
    activity = models.ForeignKey(verbose_name=u'活动名称', to=PresentSendActivity)
    exchange_code = models.CharField(verbose_name=u'兑换码', max_length=255)
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    created_user = models.ForeignKey(verbose_name=u'创建人', to=User)
    status = models.BooleanField(verbose_name=u'是否已领取', default=False)
    receiver_follower = models.ForeignKey(verbose_name=u'领取人', to=PublicFollowers,null=True)
    received_time = models.DateTimeField(verbose_name=u'领取时间',null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = '礼包领取记录'

    def __unicode__(self):
        print '%s | %s' % (self.receiver_follower, self.received_time)
