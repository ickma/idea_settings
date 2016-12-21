# coding:utf8
# @author:nick
# @company:joyme

from django.core.cache import caches
from . import PublicAccount
from . import ReplyConfigModel


def get_keywords(public):
    """
    :type public :PublicAccount
    :param public:
    :return:

    """
    if isinstance(public, PublicAccount):
        return ReplyConfigModel.get_public_keywords(public)
    raise TypeError(u'公众号实例类型错误')
