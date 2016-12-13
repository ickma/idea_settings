# coding:utf8
# @author:nick
# @company:joyme
from django.shortcuts import render
from wechat_manage.models.public_model import PublicAccount


def index(request):
    """

    :param request:
    :return:
    """
    public_index = [('id', 'id'), ('public_name', u'名称'), ('public_type', u'公众号类别') \
        , ('create_time', u'创建时间'), ('public_manage', u'进入公众号')]
    page_title = u'微信管理:后台首页'
    table_title = u'选择公众号'
    # 获取公众号信息
    publics = PublicAccount.objects.all()

    table_heads = [x[1] for x in public_index]
    table_datas = []
    for public in publics:
        # todo 将默认管理起始页改为用户管理l
        public.public_manage = '<a href="/wechat/%s/menu/create">进入管理</a>' % public.id
        line = [getattr(public, key[0]) for key in public_index]
        table_datas += [line]
    return render(request, 'base/simple_table.html', locals())
