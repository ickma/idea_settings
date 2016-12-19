# coding:utf8
# @author:nick
# @company:joyme

from django import template
from permissions.models.log_model import WebRequest
from app.menu_settings import MENU_CONFIG
from django.http import HttpRequest
from wechat_sdk import WechatBasic
from wechat_manage.models.public_model import PublicAccount
from wechat_manage.models.followers_model import PublicFollowers

# 网站统计tags
register = template.Library()


@register.simple_tag(name='visit_count')
def visit_count():
    return WebRequest.objects.count() + 1


@register.simple_tag(name='copy_right')
def copy_right_html():
    return """
     <strong>Copyright &copy; 2016 <a href="http://www.heyijoy.com/">HEYI JOYME</a>.</strong> All rights reserved.
    """


@register.simple_tag(name='side_bar', takes_context=True)
def get_side_bar(context):
    """
    
    :param context: 
    :return: 
    """
    request = context['request']  # type:HttpRequest

    public = context.get('public')
    if public and isinstance(public, WechatBasic):
        public = PublicAccount.objects.get(app_id=public.conf.appid)
    elif not public:
        public = WechatBasic()
        public.id = 0
    current_path = request.path
    html = ''
    for m in MENU_CONFIG:
        is_open = False
        li_html = ''
        for c in m['children']:
            c['path'] = c['path'].format(public.id)
            _class_name = u'class="active"' if c['path'] == current_path else u''
            if _class_name:
                is_open = True
            li_html += u'<li {class_name}><a href="{href}" >{c_name}</a></li>'.format(class_name=_class_name,
                                                                                      href=c['path'],
                                                                                      c_name=c['name'])
        html += u"""
        <li class="treeview">
        <a href=" #">
        <i class="fa fa-link"></i>
        <span>{0}</span>
        <span class="pull-right-container">
              <i class="fa fa-angle-left pull-right"></i>
            </span>
            </a>
            <ul class="treeview-menu" style="display: {2};">
                     {1}
                    </ul>
        </li>
        """.format(m['name'], li_html, u'block' if is_open else u'none')
    return html


@register.simple_tag(name='get_page_name', takes_context=True)
def get_page_name(context):
    """
    自动获取自动以的页面名称或当前url的名称
    :param context:
    :return:
    """
    page_title = context.get('page_title', None)
    if not page_title:
        request = context['request']
        from django.core.urlresolvers import resolve
        page_title = resolve(request.path).url_name
    context['page_title'] = page_title
    return page_title


@register.simple_tag(name='get_user_headimage', takes_context=True)
def get_user_headimage(context):
    """
    获取用户头像
    :return:
    """

    try:
        head_image = context['request'].user.headimgae

    except (NameError, AttributeError):
        return PublicFollowers.objects.get(id=1).headimgurl

    return head_image
