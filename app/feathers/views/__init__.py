# coding:utf8
# @author:nick
# @company:joyme
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from permissions.utils.errors import catch_error
from permissions.utils.decoraters import auth_public
from django.http import HttpRequest
