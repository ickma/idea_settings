# coding:utf8
# @author:nick
# @company:joyme
from django.conf.urls import url
from  wechat_manage.views import *

urlpatterns = [
    url(r'menu/create$', menu_manage.create, name=u'创建公众号菜单')
]
