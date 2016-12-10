# coding:utf8
# @author:nick
# @company:joyme
from django.http import HttpRequest, HttpResponse
from   django.contrib.auth.models import User

from django_wx_joyme.utils.main import get_params
from wechat_manage.models.public_model import PublicAccount
from wechat_sdk import WechatBasic


def auth_public(func):
    """
    获取public 装饰器
    :param func:
    :return:
    """

    def wrapper(func, request,public_id,*args, **kwargs):
        """

        :param func:
        :param args:
        :param kwargs:
        :return:
        """
        request = args[0]  # type:HttpRequest
        user = request.user  # type:User
        public_id = get_params(request, name='publicid')
        public_instance = PublicAccount.objects.get(id=public_id)
        # 实例化wechat_sdk实例
        wechat_instance = WechatBasic(appid=public_instance.app_id, appsecret=public_instance \
                                      .app_secret, token=public_instance.token
                                      )

        # 鉴定当前用户是否对该公众号有管理权限
        if not user.is_superuser:
            # todo 实现鉴别当前用户是否对当前公众号有管理权限
            pass

        return func(request, wechat_instance)

    return wrapper
