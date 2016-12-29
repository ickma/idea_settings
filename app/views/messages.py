# coding:utf8
# @author:nick
# @company:joyme

from . import auth_public, catch_error, login_required
from . import HttpRequest
from django.shortcuts import render
from app.models.message import Message


@login_required
# @catch_error
@auth_public
def messages(request, wechatsdk, *args):
    public_instance = args[0]
    table_datas = messages = Message.objects.filter(public=public_instance)

    return render(request, 'messages/display.html', locals())
    pass
