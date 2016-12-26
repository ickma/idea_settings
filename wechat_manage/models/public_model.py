# coding:utf8
# @author:nick
# @company:joyme
# 公众号相关model
from django.db import models
from django_wx_joyme.utils.string_util import create_random_str
from app.models.feather_models import FeatureModel
from django.contrib.admin.options import ModelAdmin


class PublicAccount(models.Model):
    # 公众号配置表

    encrypt_mode_choices = (('normal', u'明文模式'), ('compatible', u'兼容模式'), ('safe', u'安全模式'))
    public_name = models.CharField(max_length=255, verbose_name=u'公众号名称')
    token = models.CharField(max_length=255, verbose_name=u'公众号token', editable=False)
    app_id = models.CharField(max_length=255, verbose_name=u'公众号id', unique=True)
    app_secret = models.CharField(max_length=255, verbose_name=u'公众号secret')
    encrypt_mode = models.CharField(max_length=255, choices=encrypt_mode_choices, verbose_name=u'消息加解密方式')
    encrypt_aes_key = models.CharField(max_length=255, verbose_name=u'公众平台开发者选项中的 EncodingAESKey', null=True,
                                       blank=True)
    # access_token = models.CharField(max_length=255, verbose_name=u'公众号access token', null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'公众号创建时间', editable=False)
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'公众号更新时间', editable=False)
    public_type = models.CharField(max_length=25,
                                   choices=[('test', u'测试号'), ('subscribe', u'订阅号'), ('service', u'服务号')])
    public_token = models.CharField(max_length=255, verbose_name=u'公众号token码(唯一识别码)')

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
        self.token = create_random_str()
        super(PublicAccount, self).save(force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return self.public_name

    class Meta:
        verbose_name = verbose_name_plural = u'公众号配置'
        ordering = ["-id"]


class PublicMenuConfig(models.Model):
    menu_cats = [
        ('click', u'触发功能'),
        ('view', u'绑定网址'),
        ('scancode_push', u'自动扫码'),
        ('scancode_waitmsg', u'扫码事件'),
        ('pic_sysphoto', u'自动拍照发图'),
        ('pic_photo_or_album', u'拍照或相册发图'),
        ('pic_weixin', u'微信相册发图'),
        ('location_select', u'弹出地理位置选择器'),
        ('media_id', u'下发消息'),
        ('view_limited', u'跳转图文消息url')
    ]
    public = models.ForeignKey(PublicAccount, verbose_name=u'公众号')
    menu_type = models.CharField(max_length=255, choices=menu_cats, verbose_name=u'菜单类型')
    menu_name = models.CharField(max_length=255, verbose_name=u'菜单名称')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    info = models.TextField(verbose_name=u'信息内容')
    url = models.CharField(verbose_name='url', null=True, blank=True, max_length=255)
    key = models.CharField(verbose_name='key', null=True, blank=True, max_length=100)
    feather = models.ForeignKey(FeatureModel, verbose_name=u'功能外键', null=True)
    menu_level = models.IntegerField(choices=((1, u'一级菜单'), (2, u'二级菜单')))
    parent_index = models.IntegerField(verbose_name=u'父级菜单序列号')
    sync_status = models.BooleanField(verbose_name=u'同步状态', default=False)

    class Meta:
        ordering = ['parent_index']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        判断当前菜单是否超出允许的最大值：1级菜单3个，2级菜单5个
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        self.check_limit()
        #
        if bool(self.key) != self.feather:
            if self.feather:
                self.key = self.feather.feather_class
            if self.key:
                try:
                    self.feather = FeatureModel.objects.get(feather_class=self.key)
                except FeatureModel.DoesNotExist:
                    pass
        super(PublicMenuConfig, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        """
        删除方法
        删除一级菜单同步删除一级菜单下的二级菜单
        :param using:
        :param keep_parents:
        :return:
        """
        if self.menu_level == 1:
            PublicMenuConfig.objects.filter(public=self.public, menu_level=2, parent_index=self.parent_index).delete()
        super(PublicMenuConfig, self).delete()

    def check_limit(self):
        """
        检查当前菜单是否符合要求
        :return:
        """
        if self.menu_level == 1:
            if PublicMenuConfig.objects.filter(public=self.public, menu_level=1).count() >= 3:
                raise Exception(u'创建的一级菜单已经达到3个，请先进行删除操作')
        else:

            if PublicMenuConfig.objects.filter(public=self.public, parent_index=self.parent_index,
                                               menu_level=2).count() >= 5:
                raise Exception(u'当前一级菜单下创建的菜单已经达到5个，请先进行删除操作')
        return True

    @classmethod
    def get_level_one_menus(cls, public):
        """
        :param public:
        :return:
        """

        return [(x.parent_index, x.menu_name) for x in cls.objects.filter(public=public, menu_level=1)]

    @classmethod
    def get_formated_menus(cls, public):
        """

        :param public:
        :return:
        """
        parent_menus = cls.objects.filter(public=public, menu_level=1)
        menus = {'button': []}

        def formart_menu(x):
            """

            :param x:
            :type x:PublicMenuConfig
            :return:
            """
            _x = {'type': x.menu_type, 'name': x.menu_name}
            if x.key:
                _x['key'] = x.key
            if x.url:
                _x['url'] = x.url
            return _x

        for m in parent_menus:
            try:
                menu = cls.objects.filter(public=public, menu_level=2, parent_index=m.parent_index)
                assert menu.count() > 0
                menus['button'] += [{'name': m.menu_name, 'sub_button': [formart_menu(_m) for _m in menu]}]
            except AssertionError, cls.DoesNotExist:
                if m.key or m.url:
                    menus['button'] += [formart_menu(m)]

        return menus
