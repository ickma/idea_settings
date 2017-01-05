# coding:utf8
# @author:nick
# @company:joyme
from wechat_sdk import WechatBasic
from wechat_sdk.messages import EventMessage
from wechat_sdk.messages import WechatMessage
from django.db import models
from app.models.message import Message, MsgResponse
from wechat_manage.models.followers_model import PublicFollowers


class BaseFeather(object):
    """:type message_instance:WechatMessage"""

    def __init__(self, message_instance, wechatsdk, public_instance):
        """
        :type message_instance:WechatMessage|EventMessage
        :type wechatsdk:WechatBasic
        :param message_instance:
        :param wechatsdk:
        """
        self.public_instance = public_instance
        self.response_content = None
        self.response_type = None
        self.response_model_instance = None
        if isinstance(message_instance, WechatMessage):
            self.message_instance = message_instance
        else:
            # 解析当前的message
            wechatsdk.parse_data(message_instance)
            self.message_instance = wechatsdk.get_message()
            """:type message_instance:EventMessage"""
        # 绑定粉丝的model实例
        try:
            follower_instance = PublicFollowers.objects.get(public=public_instance, openid=message_instance.source)
        # 如果当前粉丝不在已获取的粉丝列表中，重新获取
        except PublicFollowers.DoesNotExist:
            #  如果当前用户不存在，则获取当前用户
            follower_info = wechatsdk.get_user_info(message_instance.target)
            follower_instance = PublicFollowers()
            for k, v in follower_info:
                setattr(follower_instance, k, v)
            follower_instance.save()
        self.follower_instance = follower_instance
        self.wechatsdk = wechatsdk

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
        实例执行方法
        :return:
        """
        response = self.get_response()
        """获取content type"""
        self.response_content = response
        response_type = self.response_type
        self.log()
        """发送响应"""
        if response_type == 'text':
            # return content
            return self.wechatsdk.response_text(content=response)

    def get_response(self):
        """获取响应"""
        raise NotImplementedError

    def log(self):
        """
        log方法
        生成msg response实例并保存
        :return:
        """
        # response 实例 MsgResponse
        response = MsgResponse(response_type=self.response_type, content=self.response_content,
                               public=self.public_instance)
        from app.models.feather_models import FeatureModel
        # 获取feather 的model 实例
        feather_model_instance = FeatureModel.objects.get(feather_class=self.message_instance.key)
        # 绑定feather实例
        response.feather = feather_model_instance
        # 保存response实例
        response.save()
        #     response实例与message实例相关联

        self.response_model_instance = response

    def __call__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        :raise BaseException
        """
        try:
            self.process()
        except Exception as e:
            raise BaseException(e)
