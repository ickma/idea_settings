# coding:utf8
# @author:nick
# @company:joyme
from . import register
from furl import furl


@register.filter(name='url_add')
def url_add(url):
    """
    设置当前
    :type url:str

    :param url:
    :return:
    """
    return furl(url).add({'action': 'add'}).url
