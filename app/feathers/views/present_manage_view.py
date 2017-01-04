# coding:utf8
# @author:nick
# @company:joyme
from app.models.feather_models import PresentSendActivity
from wechat_manage.models.public_model import PublicAccount
from . import HttpRequest, catch_error, render, login_required, auth_public
from django_wx_joyme.utils.main import get_params
from app.feathers.forms.present_manage_form import PresentForm


@login_required
@catch_error
@auth_public
def index(request, wechat_sdk, *args):
    """
    list当前所有活动
    :param wechat_sdk:
    :param request:
    :type request:HttpRequest
    :return:
    """
    user_instance = request.user
    public_instance = args[0]
    """:type:PublicAccount"""
    activities = table_datas = PresentSendActivity.objects.filter()
    action = get_params(request, name='action')
    if action == 'add':
        return add_edit(request, public_instance.id)
    table_heads = [u'序号', u'名称', u'创建时间', u'结束时间', u'当前状态']
    return render(request, 'feathers/presents/presents_admin_index.html', locals())


@login_required
@catch_error
@auth_public
def add_edit(request, wechat_sdk, *args):
    """
    编辑或新增
    :param wechat_sdk:
    :param request:
    :return:
    """
    public_instance = args[0]
    form = PresentForm()
    if request.method == 'POST':
        activity = PresentSendActivity(request.POST)

    return render(request, 'base/form.html', locals())
