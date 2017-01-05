# coding:utf8
# @author:nick
# @company:joyme

from django.conf.urls import url
from .views import present_manage_view

urlpatterns = [
    url('present/index$', present_manage_view.index, name=u'礼包发放/活动首页'),
    url('present/add$', present_manage_view.index, name=u'礼包发放/活动管理'),
    url('present/code$', present_manage_view.present_code_index, name=u'激活码管理')

]
