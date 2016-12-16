# coding:utf-8
#author:nick
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from permissions.utils.errors import catch_error


@login_required
@catch_error
def user_profile(request):
    user = request.user
    page_title = u'个人资料'
    return render(request, 'log/user_profile.html', locals())
