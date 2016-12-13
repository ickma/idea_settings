#coding:utf8
#@author:nick
#@company:joyme

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest,HttpResponse
from permissions.utils.errors import catch_error
from permissions.utils.decoraters import auth_public