# coding:utf8
# @author:nick
# @company:joyme
from django.shortcuts import render


# 当前view未实现Exception
class ViewNotReady(Exception):

    def __init__(self, *args, **kwargs):
        super(ViewNotReady, self).__init__(*args, **kwargs)

    def __unicode__(self):
        """
        :return:
        """
        return u'功能未实现'
