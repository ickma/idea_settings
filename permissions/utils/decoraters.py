# coding:utf8
# @author:nick
# @company:joyme
from django.http import HttpRequest, HttpResponse
from   django.contrib.auth.models import User

from django_wx_joyme.utils.main import get_params
from wechat_manage.models.public_model import PublicAccount
from wechat_sdk import WechatBasic
from django.conf import settings
from django.core.cache import cache
from django.conf import settings


def auth_public(func):
    """
    获取public 装饰器
    :param func:
    :return:
    """

    def wrapper(request, publicid, *args, **kwargs):
        """

        :param publicid:
        :param func:
        :type request:HttpRequest
        :param args:
        :param kwargs:
        :return:
        """
        user = request.user  # type:User
        try:
            # public_id = get_params(request, name='publicid')
            public_instance = PublicAccount.objects.get(id=int(publicid))
        except (AttributeError, TypeError):
            raise Exception(u'未选择公众号')
        except PublicAccount.DoesNotExist:
            raise Exception(u'选择的公众号不存在')

        # 实例化wechat_sdk实例
        # 获取缓存项
        cache_access_token_name = '%s_public_%s_access_token' % (settings.APP_NAME, public_instance.token)
        cached_access_token = cache.get(cache_access_token_name, {})
        cache_js_ticket_name = cache_access_token_name.replace('access_token', 'js_ticket')
        cached_ticket = cache.get(cache_js_ticket_name, {})
        access_token = cached_access_token.get('access_token')
        access_token_expire_at = cached_access_token.get('access_token_expires_at')
        jsapi_ticket = cached_ticket.get('jsapi_ticket')
        jsapi_ticket_expires_at = cached_ticket.get('jsapi_ticket_expires_at')

        wechat_instance = WechatBasic(appid=public_instance.app_id, appsecret=public_instance \
                                      .app_secret, token=public_instance.token, access_token=access_token,
                                      jsapi_ticket=jsapi_ticket,
                                      access_token_expires_at=access_token_expire_at,
                                      jsapi_ticket_expires_at=jsapi_ticket_expires_at
                                      )
        access_token = wechat_instance.get_access_token()
        jsapi_ticket = wechat_instance.get_jsapi_ticket()

        # 缓存access token
        if not cached_access_token or not cached_ticket:
            cache.set(cache_access_token_name, access_token, 7200 - 100)
            cache.set(cache_js_ticket_name, jsapi_ticket, 7200 - 100)

        # 鉴定当前用户是否对该公众号有管理权限
        if not user.is_superuser:
            # todo 实现鉴别当前用户是否对当前公众号有管理权限
            pass
        args = [public_instance]
        return func(request, wechat_instance, *args)

    return wrapper
