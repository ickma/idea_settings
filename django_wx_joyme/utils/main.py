# coding:utf8
# @author:nick
# @company:joyme
from django.http import HttpRequest, HttpResponse


def get_params(request=None, name='', method='get', default=None, formatter=None, need_strip=True, required=False,
               get_list=False):
    """
    获取参数
    :param request: request 对象
    :type request :HttpRequest
    :param name: 参数名
    :type name:str
    :param method: 请求方式 get|post
    :type method:str
    :param default: 默认值
    :param formatter: 默认格式化函数
    :type formatter:function
    :param need_strip: 是否去除两端空格
    :type need_strip:bool
    :param required: 是否必须
    :type required:bool
    :param get_list: 是否获取list，默认获取单个值
    :type get_list:bool
    :return:
    :rtype:object
    :raises :KeyError
    """
    if request is None or name == '':
        value = default
    # 获取当参数
    else:
        if method == 'get':
            value = request.GET.getlist(key=name, default=default) if get_list else  request.GET.get(key=name,
                                                                                                     default=default)
        else:
            value = request.POST.getlist(key=name, default=default) if get_list else request.POST.get(key=name,
                                                                                                      default=default)
    # 清除两端空格
    if need_strip:
        if isinstance(value, list):
            value = [v.strip for v in value]
        else:
            value = value.strip()
    # 格式化当前参数
    if value is not None and formatter:
        try:
            if isinstance(value, list):
                value = [formatter(v) for v in value]
            else:
                value = formatter(value)
        except Exception:
            raise Exception(u'无法对当前参数进行格式化处理')
    # 判断当前参数是否为空值
    if required and not value:
        raise KeyError(u'未获取到正确的参数值')
