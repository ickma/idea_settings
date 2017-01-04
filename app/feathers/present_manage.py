# coding:utf8
# @author:nick
# @company:joyme
from . import BaseFeather
from . import WechatBasic
from django.shortcuts import render


class Present(BaseFeather):
    """实现发放礼包功能"""
    """一个用户只能领1次"""
    """每天发多少不做限制"""
    """活动能随时关停"""
    """活动能配置结束提示语"""
    """活动能配置礼包发放完提示语"""

    """能查询剩余多少未发，可以追加"""
    """只能通过菜单栏、关键字领取"""


    @staticmethod
    def manage(request):
        """
        活动管理方法
        :param request:
        :return:
        """
        return render(request, 'feathers/presents/presents_admin_index.html', locals())

    def view_presents(self):
        """
        查看已上传的礼包方法
        :return:
        """
        return self
        pass

    def presents_receive(self):
        """
        查看用户已领取的礼包
        :return:
        """
        return self
        pass

    def upload_presents(self):
        """
        上传礼包的view 方法
        :return:
        """
        return self
        pass

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
