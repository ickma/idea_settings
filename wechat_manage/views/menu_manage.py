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
from wechat_manage.models.public_model import PublicMenuConfig
from wechat_manage.forms.menu_form import MenuCreateForm
import json
from wechat_manage.utils.menu_utils import menu_info_format


@login_required
@catch_error
@auth_public
def sync_menus(request, wechatsdk, *args):
    """
    从服务器同步菜单设置
    :param request:
    :param wechatsdk:
    :param args:
    :return:
    """
    public_instance = args[0]
    #  获取服务器菜单配置
    menu_settings = wechatsdk.get_menu()['menu']['button']

    menus = []
    # 获取菜单配置
    for n, m in enumerate(menu_settings):
        #  格式化1级菜单
        menus += [dict(m.items() + [('parent_index', n), ('menu_level', 1)])]
        #  格式化2级菜单
        if m['sub_button']:
            # menus += [x.update({'parent_index': n, 'menu_level': 2}) for x in m['sub_button']]
            menus += [dict(x.items() + [('parent_index', n), ('menu_level', 2)]) for x in
                      m['sub_button']]  # type:list[dict]

    # 清空数据库
    PublicMenuConfig.objects.filter(public=public_instance).delete()
    # 保存到数据库
    for m in menus:
        menu_instance = PublicMenuConfig()
        menu_instance.public = public_instance
        menu_instance.menu_level = m['menu_level']
        menu_instance.menu_type = m.get('type', '')
        menu_instance.url = m.get('url', '')
        menu_instance.key = m.get('key', '')
        menu_instance.menu_name = m['name']
        menu_instance.parent_index = m['parent_index']
        menu_instance.sync_status = True
        menu_instance.save()
    success_msg = u'菜单已更新成功'

    return render(request, 'error/success.html', locals())


@login_required
# @catch_error
@auth_public
def display(request, wechatsdk, *args):
    """
    创建公众号菜单
    :param wechatsdk:
    :type wechatsdk:WechatBasic
    :param request:request实例
    :type request:HttpRequest

    :return:
    """
    page_title = u'菜单设置'
    public_instance = args[0]
    action = get_params(request, name='action')
    if action == 'add':
        return menu_add(request, public_instance.id)
    if action == 'edit':
        return menu_edit(request, public_instance.id)
    if action == 'delete':
        menu_id = get_params(request, name='id', formatter=int)
        PublicMenuConfig.objects.get(pk=menu_id).delete()
        return render(request, 'error/success.html', locals())
    table_datas = menus = PublicMenuConfig.objects.filter(public=public_instance)
    return render(request, 'wechat_menus/display.html', locals())


@login_required
# @catch_error
@auth_public
def menu_add(request, public, *args):
    """
    为公众号增加菜单
    :type request:HttpRequest
    :type public:WechatBasic
    :param request: 
    :param public: 
    :return: 
    """
    public_instance = PublicAccount.objects.get(app_id=public.conf.appid)
    page_title = u'增加菜单'
    menu_level = get_params(request, name='level', formatter=int, default=2)
    parent_id = get_params(request, name='parentid', formatter=int, default=0)
    if request.method == 'POST':
        menu_instance = PublicMenuConfig()
        menu_id = get_params(request, method='get', name='id', formatter=int)
        if menu_id:
            try:
                menu_instance = PublicMenuConfig.objects.get(pk=menu_id)
            except menu_instance.DoesNotExist:
                pass
        menu_instance.menu_name = get_params(request, method='post', name='menu_name')
        menu_instance.feather_id = get_params(request, method='post', name='feathers', formatter=int)
        menu_instance.url = get_params(request, method='post', name='url')
        menu_instance.menu_type = get_params(request, method='post', name='menu_cates')
        menu_instance.public = public_instance
        if not menu_instance.id:
            menu_instance.menu_level = get_params(request, method='post', name='menu_level')
            menu_instance.parent_index = get_params(request, method='post', name='parent_menu', formatter=int)
        menu_info_format(menu_instance)
        menu_instance.save()

        return render(request, 'error/success.html', locals())
    if request.method == 'GET':
        # 判断当前的菜单是否有超过规定数量
        form_method = 'post'
        form = MenuCreateForm(initial={'menu_level': menu_level}, public=public_instance)
        return render(request, 'wechat_menus/add_edit.html', locals())


@login_required
# @catch_error
@auth_public
def menu_edit(request, public, *args):
    """
    编辑菜单
    :param request:
    :param public:
    :return:
    """
    public_instance = args[0]
    """:type:PublicAccount"""
    if request.method == 'POST':
        return menu_add(request, public_instance.id)
    page_title = u'编辑公众号菜单'
    form_method = 'post'
    menu_id = get_params(request, name='id', formatter=int, default=0)
    if menu_id:
        try:
            menu_instance = PublicMenuConfig.objects.get(pk=menu_id)
        except PublicMenuConfig.DoesNotExist:
            error_msg = u"当前id不存在对应的菜单"
            return render(request, 'error/error.html', locals())
    else:
        menu_instance = PublicMenuConfig()
    menu_init = {
        'menu_level': menu_instance.menu_level,
        'menu_type': menu_instance.menu_type,
        'menu_name': menu_instance.menu_name,
        'menu_info': menu_instance.info,
        'parent_menu': menu_instance.parent_index,
        'url': menu_instance.url,
        'key': menu_instance.key
    }
    form = MenuCreateForm(initial=menu_init, action='edit')
    if menu_instance.menu_level == 1:
        _ = form.fields.pop('parent_menu')
    return render(request, 'wechat_menus/add_edit.html', locals())


@login_required
# @catch_error
@auth_public
def menu_push(request, wechatsdk, *args):
    """

    :param wechatsdk:
    :type wechatsdk:WechatBasic
    :param request:
    :param args:
    :return:
    """

    menus = PublicMenuConfig.get_formated_menus(public=args[0])
    wechatsdk.create_menu(menus)
    success_msg = u'提交成功 请使用拉取菜单功能从服务器获取最新菜单配置'
    return render(request, 'error/success.html', locals())
