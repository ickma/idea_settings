# coding:utf8
# @author:nick
# @company:joyme
from app.models.feather_models import PresentSendActivity, Present
from wechat_manage.models.public_model import PublicAccount
from . import HttpRequest, catch_error, render, login_required, auth_public
from django_wx_joyme.utils.main import get_params
from app.feathers.forms.present_manage_form import PresentForm, PresentCodeImportForm
from datetime import datetime


@login_required
# @catch_error
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
    action = get_params(request, name='action')
    if action:
        return add_edit(request, public_instance.id)

    activities = table_datas = PresentSendActivity.objects.filter(public=public_instance)
    table_heads = [u'序号', u'名称', u'创建时间', u'开始时间', u'结束时间', u'当前状态', u'激活码管理', u'操作']
    return render(request, 'feathers/presents/presents_admin_index.html', locals())


@login_required
# @catch_error
@auth_public
def add_edit(request, wechat_sdk, *args):
    """
    编辑或新增活动
    :param activity_id:
    :param wechat_sdk:
    :param request:
    :return:
    """
    public_instance = args[0]
    form = PresentForm()
    activity_id = get_params(request, name='id', formatter=int)
    if activity_id:
        activity_instance = PresentSendActivity.objects.get(pk=activity_id)
        form = PresentForm(instance=activity_instance)
    form_method = 'post'
    if request.method == 'POST':
        from datetime import datetime
        _format = '%Y-%m-%d %H:%M:%S'
        request.POST['start_date'] = datetime.strptime(request.POST['start_date'], _format)
        request.POST['end_date'] = datetime.strptime(request.POST['end_date'], _format)

        request.POST.update({'create_user': request.user, 'public': public_instance})
        activity = PresentForm(request.POST)
        if activity_id:
            activity = PresentForm(request.POST, instance=activity_instance)
        if activity.is_valid():
            _activity = activity.save(commit=False)
            _activity.public = public_instance
            _activity.create_user = request.user
            _activity.save()
            activity.save_m2m()
        else:
            raise Exception(activity.errors)
        return render(request, 'error/success.html', locals())

    return render(request, 'base/form.html', locals())


@login_required
@catch_error
def present_code_index(request, publicid):
    activity_id = get_params(request, name='activityid', formatter=int)
    action = get_params(request, name='action')
    if action == 'add':
        return present_code_import(request, activity_id)
    present_codes = Present.objects.filter(activity__id=activity_id)

    table_heads = [u'序号', u'活动名称', u'激活码创建时间', u'创建人', u'激活码信息', u'领取状态', u'领取时间', u'领取人']
    table_datas = present_codes
    return render(request, "feathers/presents/present_codes_index.html", locals())


def present_code_import(request, activity_id):
    """
    上传激活码方法
    :param request:
    :param activity_id:
    :return:
    """
    form = PresentCodeImportForm()
    if request.method == 'POST':
        form = PresentCodeImportForm(files=request.FILES)
        activity = PresentSendActivity.objects.get(pk=activity_id)
        if form.is_valid():
            # todo 读取上传文件
            # 获取上传文件
            codes = form.cleaned_data['codes'].file.read().split('\n')
            for code in codes:
                if code:
                    code = Present(activity=activity, exchange_code=code, created_user=request.user)
                    code.save()
            success_msg = u'上传成功'
            return render(request, 'error/success.html', locals())

    form_method = 'post'

    return render(request, 'base/form.html', locals())
