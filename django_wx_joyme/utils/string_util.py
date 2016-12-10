# coding:utf8
# @author:nick
# @company:joyme
import string
import random


def create_random_str(length=20):
    """
    生成随机字符串
    :param length:
    :type length:20
    :return:
    """
    if isinstance(length, int):
        length = 20
    return ''.join([random.choice(string.letters + string.digits) for n in range(length)])
