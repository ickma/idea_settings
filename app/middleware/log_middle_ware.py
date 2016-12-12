# coding:utf8
# @author:nick
# @company:joyme
from permissions.utils.log_module import log_each_visit
from django.http import HttpRequest,HttpResponse
import sys


def log_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        """
        :type request:HttpRequest
        :param request:
        :return:
        """
        # Code to be executed for each request before

        response = get_response(request)
        if request.path != '/favicon.ico':
            log_each_visit(request, response)

        # the view (and later middleware) are called.
        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
