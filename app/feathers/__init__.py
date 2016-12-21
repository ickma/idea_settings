# coding:utf8
# @author:nick
# @company:joyme
from wechat_sdk import WechatBasic
from django.db import models


class BaseFeather(object):
    def __init__(self, public):
        self.public = public

    @property
    def model(self):
        return self.model

    @model.setter
    def model(self, value):
        if isinstance(value, models.Model):
            self.model = value
        else:
            raise TypeError(u'不是被支持的模型类')

    @model.deleter
    def model(self):
        self.model = None

    def process(self):
        """
        实现
        :return:
        """
        raise NotImplementedError

    def log(self):
        """
        log
        :return:
        """
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        try:
            self.process()
            self.log()
        except Exception as e:
            raise BaseException(e)
