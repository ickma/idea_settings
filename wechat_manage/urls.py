# coding:utf8
# @author:nick
# @company:joyme
from django.conf.urls import url
from  wechat_manage.views.menu_manage import display as menu_display
from wechat_manage.views.menu_manage import menu_add, menu_edit, sync_menus

from wechat_manage.views.user_manage import sync_followers, user_index

from wechat_manage.views.reply import welcome_reply, keywords_reply
from wechat_manage.views.material_manage import material_manage

urlpatterns = [
    url(r'menu/sync', sync_menus, name=u'同步菜单配置'),
    url(r'menu/display$', menu_display, name=u'显示公众号菜单配置'),
    url(r'menu/add$', menu_add, name=u'增加公众号菜单'),
    url(r'menu/edit$', menu_edit, name=u'编辑公众号菜单'),
    url(r'reply/welcome', welcome_reply, name=u'编辑关注欢迎语'),
    url(r'reply/keyword', keywords_reply, name=u'编辑关键词回复'),
    url(r'followers/query$', user_index, name=u'全部粉丝'),
    url(r'followers/sync$', sync_followers, name=u'同步粉丝'),
    url(r'material/manage', material_manage, name=u'多媒体素材管理')

]
