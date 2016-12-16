# coding:utf8
# @author:nick
# @company:joyme
from django.http import HttpRequest
from permissions.models.log_model import LogModel
# from django.core import serializers
from django.contrib.auth.models import User,AnonymousUser

import json
from permissions.models.log_model import WebRequest
from  django.http import HttpResponse


def log_each_visit(request, response):
    """
    将每次请求写入log model
    :param response:
    :type request:HttpRequest
    :param request:
    :return:
    """
    if type(response) == HttpResponse:
        log_instance = LogModel()
        if not isinstance(request.user,AnonymousUser):
            log_instance.user = request.user
        log_instance.path = request.path
        log_instance.request = request_to_model(request=request, response=response)

        log_instance.save()


def request_to_model(request, response):
    """
    :param response:
    :type request:HttpRequest
    :param request:
    :return:
    """

    def dumps(value):
        return json.dumps(value, default=lambda o: None)

    meta = request.META
    remote_addr_fwd = ''
    if 'HTTP_X_FORWARDED_FOR' in meta:
        remote_addr_fwd = meta['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
        if remote_addr_fwd == meta['HTTP_X_FORWARDED_FOR']:
            meta.pop('HTTP_X_FORWARDED_FOR')
    request_instance = WebRequest()
    request_instance.path = request.path
    request_instance.host = request.get_host()
    request_instance.method = request.method
    request_instance.uri = request.build_absolute_uri()
    request.status_code = response.status_code
    request_instance.user_agent = meta.pop('HTTP_USER_AGENT', None)
    request_instance.remote_addr = meta.pop('REMOTE_ADDR', None)
    request_instance.remote_addr_fwd = remote_addr_fwd
    request_instance.meta = None if not meta else dumps(meta)
    request_instance.cookies = None if not request.COOKIES else dumps(request.COOKIES)
    request_instance.get = None if not request.GET else dumps(request.GET)
    request_instance.post = None if (not request.POST or getattr(request, 'hide_post',None) == True) else dumps(
        request.POST)
    # request_instance.raw_post = None if getattr(request, 'hide_post') else request.raw_post_data,
    request_instance.raw_post = None
    request_instance.is_secure = request.is_secure()
    request_instance.status_code=response.status_code
    request_instance.is_ajax = request.is_ajax()
    request_instance.user = request.user  if not isinstance(request.user,AnonymousUser) else None
    request_instance.save()
    return request_instance
