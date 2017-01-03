# coding:utf8
# @author:nick
# @company:joyme
from . import BaseFeather
from present_manage import Present
from present_manage import Test
from funny import Funny


class FeatherProxy(object):
    """Feather 调用实例代理l"""
    feathers = {}

    @classmethod
    def register(cls, feather_name, feather):
        """
        :type feather:BaseFeather
        :type feather_name:str
        :param feather_name: 功能类名
        :param feather: 功能cls
        :return:
        """
        feather_name = feather_name.lower()
        if cls.feathers.get(feather_name):
            raise KeyError('already registered')
        else:
            if issubclass(feather, BaseFeather):
                cls.feathers.update({feather_name: feather})
            else:
                raise TypeError('传入实例不正确')

    @classmethod
    def get_feather(cls, feather_name):
        """
        输出feather
        :return:
        :rtype :BaseFeather
        """
        feather_name = feather_name.lower()
        try:
            feather = cls.feathers[feather_name]
            if issubclass(feather, BaseFeather):
                return cls.feathers[feather_name]
            else:
                raise TypeError('注册的实例不正确')
        except KeyError:
            raise KeyError('请求的功能不存在或未注册')

    @classmethod
    def feather_exists(cls, feather_name):
        """
        判断当前功能类是否被注册进proxy
        :type feather_name:str
        :param feather_name:
        :return:
        """
        try:
            if cls.get_feather(feather_name.lower()):
                return True
        except KeyError:
            pass
        finally:
            return False


"""注册present功能"""
FeatherProxy.register('Present', Present)
"""注册Test功能"""
FeatherProxy.register('Test', Test)
"""注册其它Feather"""
FeatherProxy.register('Funny', Funny)
