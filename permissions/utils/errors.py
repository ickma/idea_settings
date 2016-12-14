# coding:utf8
# @author:nick
# @company:joyme

from django.shortcuts import render


def catch_error(func):
    """
        Decorator for views that catch exceptions and return http response error with exception information.
    :param func:

    :return:
    """

    def wrapper(request, *args, **kwargs):
        try:
            _ = func(request, *args, **kwargs)
            return _
        except Exception as e:
            error_msg = u'出错原因:%s' % e
            page_title = u'出错提示'
            return render(request, 'error/error.html', locals())

    return wrapper


def _catch_error(func):
    """
    Decorator for views that catch exceptions and return http response error with exception infomation.
    """

    def wrapper(request, *args, **kwargs):
        try:
            ret_val = func(request, *args, **kwargs)
            """下载excel"""
            return ret_val
        except Exception, err:
            return render(request, "error/error.html", {"errmsg": str(err)})

    return wrapper
