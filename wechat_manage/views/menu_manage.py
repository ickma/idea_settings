# coding:utf8
# @author:nick
# @company:joyme

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from wechat_manage.models.public_model import PublicAccount
from django_wx_joyme.utils.main import get_params
from permissions.utils.decoraters import auth_public
from django.contrib.auth.decorators import login_required
from wechat_sdk import WechatBasic
from wechat_manage.forms.menu_form import MenuCreate


@login_required
@auth_public
def create(request, public):
    """
    创建公众号菜单
    :param request:request实例
    :type request:HttpRequest
    :type public:WechatBasic
    :param public:公众号实例
    :return:
    """
    form = MenuCreate()
    return render(request, locals())
