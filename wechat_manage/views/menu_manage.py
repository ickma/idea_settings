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
# @catch_error
@auth_public
def display(request, public, *args):
    """
    创建公众号菜单
    :param public: public 实例
    :type public:WechatBasic
    :param request:request实例
    :type request:HttpRequest

    :return:
    """
    page_title = u'菜单设置'
    public_instance = PublicAccount.objects.get(app_id=public.conf.appid)
    menu_settings = public.get_menu()['menu']['button']
    menus = []
    # 获取菜单配置
    for n, m in enumerate(menu_settings):
        menus += [dict(m.items() + [('parent_index', n), ('menu_level', 1)])]
        if m['sub_button']:
            # menus += [x.update({'parent_index': n, 'menu_level': 2}) for x in m['sub_button']]
            menus += [dict(x.items() + [('parent_index', n), ('menu_level', 2)]) for x in
                      m['sub_button']]  # type:list[dict]

    # 情况数据库
    PublicMenuConfig.objects.filter(public=public_instance).delete()
    # 保存到数据库
    for m in menus:
        menu_instance = PublicMenuConfig()
        menu_instance.public = public_instance
        menu_instance.menu_level = m['menu_level']
        menu_instance.menu_type = m.get('type', '')
        menu_instance.menu_name = m['name']
        menu_instance.info = json.dumps(m)
        menu_instance.parent_index = m['parent_index']
        menu_instance.save()
    menus = PublicMenuConfig.objects.filter(public=public_instance)

    # form = MenuCreateForm(initial=request.GET)

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
        menu_instance.menu_name = get_params(request, method='post', name='menu_name')
        menu_instance.menu_level = get_params(request, method='post', name='menu_level')
        menu_instance.menu_type = get_params(request, method='post', name='menu_cates')
        menu_instance.info = get_params(request, method='post', name='menu_info')
        menu_instance.public = public_instance
        menu_instance.parent_index = get_params(request, method='post', name='parent_menu')
        menu_info_format(menu_instance)
        menu_instance.save()

    if request.method == 'GET':
        form_method = 'post'
        parent_name = PublicMenuConfig.objects.get(id=parent_id).menu_name if menu_level == 2 else ''
        # 判断当前的菜单是否有超过规定数量

        form = MenuCreateForm(initial={'menu_level': menu_level, 'parent_menu': parent_name})

        return render(request, 'wechat_menus/add_edit.html', locals())


@login_required
@catch_error
@auth_public
def menu_edit(request, public, *args):
    """

    :param request:
    :param public:
    :return:
    """
    public_instance = args[0]
    page_title = u'编辑公众号菜单'
    menu_id = get_params(request, name='id', formatter=int, default=0)
    if menu_id:
        try:
            menu_instance = PublicMenuConfig.objects.get(id=menu_id)
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
        'parent_menu': menu_instance.parent_index
    }
    form = MenuCreateForm(initial=menu_init)
    if menu_instance.menu_level == 1:
        _ = form.fields.pop('parent_menu')
    return render(request, 'wechat_menus/add_edit.html', locals())
    if request.method == 'POST':
        pass
    all_menus = PublicMenuConfig.objects.filter(public=public_instance)
    return render(request, 'wechat_manage/menu_display.html', locals())
