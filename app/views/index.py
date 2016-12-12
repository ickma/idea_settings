# coding:utf8
# @author:nick
# @company:joyme
from django.shortcuts import render


def index(request):
    page_title = u'微信管理后台首页'
    return render(request, 'base/index.html', locals())
