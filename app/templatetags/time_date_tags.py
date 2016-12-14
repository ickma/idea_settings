# coding:utf8
# @author:nick
# @company:joyme

from . import register
import time
import datetime


@register.filter(name='ts_to_str')
def ts_format(v):
    """
     格式化时间戳
     将时间戳格式化为  '%Y%m%d %H:%M:%I'格式的字符串
     :param v:
     :return:
     """
    try:
        v = int(v)
    except (ValueError, TypeError):
        return v
    import datetime
    return datetime.datetime.fromtimestamp(int(v)).strftime('%Y-%m-%d %H:%M:%S')
