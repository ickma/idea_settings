# coding:utf8
# @author:nick
# @company:joyme
from . import BaseFeather
from . import WechatBasic


class Present(BaseFeather):
    """Present"""

    def get_response(self):
        pass


class Test(BaseFeather):
    """Test"""

    def get_response(self):
        """

        :return:
        """
        self.response_type = 'text'
        return u'啪啪以啪啪 啊啊啊啊啊 摩擦以摩擦 啊啊啊啊啊'
