#coding:utf8
#@author:nick
#@company:joyme
from wechat_sdk import WechatConf
from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from wechat_sdk import WechatBasic
from django_wx_joyme.utils.main import get_params
from permissions.utils.errors import catch_error
from permissions.utils.decoraters import auth_public
from django.contrib.auth.decorators import login_required