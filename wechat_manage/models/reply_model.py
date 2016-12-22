# coding:utf8
# @author:nick
# @company:joyme
from django.db import models
from .public_model import PublicAccount
from app.models.feather_models import FeatureModel


class ReplyConfigModel(models.Model):
    # 公众号回复设置模型
    content_type_choices = [(1, u'文本'), (2, u'图片'), (3, u'语音'), (4, u'图文素材'), (5, u'视频'), (6, u'功能配置')]
    reply_type_choices = [(1, u'关注回复'), (2, u'默认回复'), (3, u'关键字回复')]
    public = models.ForeignKey(PublicAccount, verbose_name=u'公众号')
    name = models.CharField(verbose_name=u'名称', max_length=255, null=True, blank=True, unique=True)
    content_type = models.IntegerField(verbose_name=u'回复类型', choices=content_type_choices)
    reply_type = models.IntegerField(verbose_name=u'回复类型', choices=reply_type_choices)
    reply_content = models.TextField(verbose_name=u'回复内容', null=True, blank=True)
    file = models.FileField(verbose_name=u'回复文件', blank=True, null=True)
    feather = models.ForeignKey(verbose_name=u'功能', to=FeatureModel, null=True)
    keywords = models.TextField(verbose_name=u'关键字', blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u'公众号回复设置'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.reply_type == 3 and not self.keywords:
            raise ValueError(u'关键字不能为空')
        if not self.content and not self.file and not self.feather:
            raise ValueError(u'回复内容未选择或正确')
        if self.get_content_type_display() == u'功能配置':
            self.file = self.content = None

        if self.content_type == 1:
            self.file = None
            self.feather = None
        elif self.content_type != 6:
            self.feather = None
            self.content = None
        super(ReplyConfigModel, self).save(force_insert, force_update, using, update_fields)

    def get_feather_id(self):
        """
        获取当前的featehr id
        :return:
        """
        if self.feather:
            return self.feather.id
        else:
            return None

    @classmethod
    def get_public_keywords(cls, public):
        """
        返回当前公众号下的所有已定义的关键字
        :type public:PublicAccount
        :param public:
        :return:
        """
        key_words = [x.split('\n') for x in cls.objects.filter(public=public)]
        return reduce(lambda z, y: z + y, key_words)


