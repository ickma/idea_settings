# coding:utf8
# @author:nick
# @company:joyme

from django.shortcuts import render


def catch_error(func):
    """

    :return:
    """

    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as e:
            error_msg = u'出错原因:%s' % e
            page_title = u'出错提示'
            return render(request, 'error/error.html', locals())

    return wrapper
