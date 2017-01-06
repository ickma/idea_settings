# coding:utf8
# @author:nick
# @company:joyme

from . import WechatBasic
from wechat_sdk import messages
from wechat_sdk.messages import EventMessage, TextMessage, ImageMessage, LinkMessage \
    , VideoMessage, VoiceMessage, ShortVideoMessage, LocationMessage
from app.feathers import BaseFeather
from app.models.message import Message, MsgResponse
from wechat_manage.models.public_model import PublicAccount
from wechat_manage.models.reply_model import ReplyConfigModel
from wechat_manage.models.followers_model import PublicFollowers


class Reply(object):
    """Reply 实例"""
    hint_word = None
    _is_hint = False
    hint_keyword_instance = None
    """:type hint_keyword_instance :ReplyConfigModel"""
    _response_type = None
    _response_content = None
    _response_msgid = None
    feather = None
    """:type feather:"""

    def __init__(self, message_instance, public_instance, wechatsdk_instance, follower_instance):
        """
        :type follower_instance: PublicFollowers
        :type wechatsdk_instance: WechatBasic
        :type message_instance:Message
        :type public_instance:PublicAccount
        :param message_instance:
        :param public_instance:
        """
        # 实例化新的response类
        self.follower_instance = follower_instance
        self.messages_response_instance = MsgResponse()
        if isinstance(wechatsdk_instance, WechatBasic):
            self.wechatsdk_instance = wechatsdk_instance
        else:
            raise TypeError(u'wechatsdk 类型不正确')
        if isinstance(message_instance, Message):
            self.message_instance = message_instance
        else:
            raise TypeError(u'message_instance 类型不正确')
        if isinstance(public_instance, PublicAccount):
            self.public_instance = public_instance
        else:
            raise TypeError(u'public_instance 类型不正确')

        # message_response 添加public 属性
        self.messages_response_instance.public = public_instance
        # 处理event事件推送
        if isinstance(self.message_instance.msg_instance, EventMessage):
            self._get_feather()

        # 处理普通用户消息
        else:
            self._keywords = ReplyConfigModel.get_public_keywords(self.public_instance)
            self._get_hint_word()
        super(Reply, self).__init__()

    def __call__(self, *args, **kwargs):
        self.reply()
        return self

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, value):
        pass

    def _get_feather(self):
        """
        获取当前事件对应的功能实例
        :return:
        """
        from app.feathers.feather_proxy import FeatherProxy
        # 根据消息中的key值获取对应的功能cls
        self.feather_cls = FeatherProxy.get_feather(self.message_instance.msg_instance.key)
        # 实例化当前功能类
        self.feather = self.feather_cls(message_instance=self.message_instance.msg_instance,
                                        wechatsdk=self.wechatsdk_instance, public_instance=self.public_instance,
                                        follower_instance=self.follower_instance)
        """:type feather:BaseFeather"""

    def _get_hint_word(self):
        """
        获取命中的关键字
        规则为命中到第1个即退出
        :return:
        """
        if self.message_instance.type == 'text':
            word = self.message_instance.content.strip()
            for i, w in self._keywords:
                if word in w:
                    # 保存命中关键字
                    self.hint_word = word
                    # 保存命中规则实例
                    self.hint_keyword_instance = i
                    self._hint_type = 'keywords'
                    # 更新是否命中状态
                    self._is_hint = True
                    return w
        return None

    def reply(self):
        """
        回复方法
        :return:
        """
        # 处理时间推送
        if self.feather:
            # 执行事件响应
            response = self.feather.process()
            """设置响应模型的response content"""
            """response"""
            self.messages_response_instance = self.feather.response_model_instance
            return response
        if self._is_hint:
            response = self._reply()
            # 为msg response 添加属性
            self.messages_response_instance.keywords = self.hint_word
            self.messages_response_instance.response_type = self._response_type
            self.messages_response_instance.content = self._response_content
            self.messages_response_instance.msg = self._response_msgid
            self.messages_response_instance.save()
            return response
        return ''

    def _reply(self):
        """
        :return:
        """

        if self.hint_keyword_instance.content_type == 1:
            self._response_type = 'text'
            self._response_content = self.hint_keyword_instance.reply_content
            return self.wechatsdk_instance.response_text(self.hint_keyword_instance.reply_content)
