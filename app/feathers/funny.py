# coding:utf8
# @author:nick
# @company:joyme
from . import BaseFeather


class Funny(BaseFeather):
    def get_response(self):
        followers_openid = str(self.message_instance.source)
        self.response_type = 'text'
        dick_length = ord(followers_openid[-1]) / 10
        percents = 53.22 + dick_length
        return u'你的JJ长度%scm，大于全球%s%%的人' % (dick_length+10, percents)
