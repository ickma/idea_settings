# coding:utf8
# @author:nick
# @company:joyme

from . import WechatBasic
from wechat_sdk import messages
from app.models.message import Message, MsgResponse
from wechat_manage.models.public_model import PublicAccount
from wechat_manage.models.reply_model import ReplyConfigModel


class Reply(object):
    hint_word = None
    _is_hint = False
    hint_keyword_instance = None
    """:type:ReplyConfigModel"""
    _response_type = None
    _response_content = None
    _response_msgid = None

    def __init__(self, message_instance, public_instance, wechatsdk_instance):
        """

        :param message_instance:
        :param public_instance:
        """
        # 实例化新的response类
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
