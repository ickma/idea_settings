# coding:utf8
# @author:nick
# @company:joyme
from django.conf.urls import url
from  wechat_manage.views.menu_manage import create as menu_create
from wechat_manage.views.user_manage import sync_followers, user_index

urlpatterns = [
    url(r'menu/create$', menu_create, name=u'创建公众号菜单'),

    url(r'followers/query$', user_index, name=u'全部粉丝'),
    url(r'followers/sync$', sync_followers, name=u'同步粉丝'),

]
