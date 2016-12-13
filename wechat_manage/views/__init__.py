#coding:utf8
#@author:nick
#@company:joyme
from wechat_sdk import WechatConf
from . import menu_manage
from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from wechat_sdk import WechatBasic
from django_wx_joyme.utils.main import get_params