# coding:utf8
# @author:nick
# @company:joyme

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from permissions.utils.errors import catch_error
from wechat_manage.models.public_model import PublicAccount
from django_wx_joyme.utils.main import get_params
from permissions.utils.decoraters import auth_public
from django.contrib.auth.decorators import login_required
from wechat_sdk import WechatBasic
from wechat_manage.forms.menu_form import MenuCreate


@login_required
# @catch_error
@auth_public
def create(request, public):
    """
    创建公众号菜单
    :param public: public 实例
    :type public:WechatBasic
    :param request:request实例
    :type request:HttpRequest

    :return:
    """
    page_title = u'菜单设置'
    menu_settings = public.get_menu()

    # form = MenuCreate(initial=request.GET)

    return render(request, 'base/simple_table.html', locals())
