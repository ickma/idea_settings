# coding:utf8
# @author:nick
# @company:joyme
from . import get_params, catch_error, auth_public, login_required
from wechat_manage.forms import material_form
from . import HttpRequest, WechatBasic, render
from wechat_manage.models.public_model import PublicAccount
from wechat_manage.forms.material_form import MaterialMediaForm
from wechat_manage.models.material_model import MediaModel
from django.core.files import File


@login_required
# @catch_error
@auth_public
def material_manage(request, public, *args):
    """

    :param request:
    :param public:
    :param args:
    :type request :HttpRequest
    :type public:WechatBasic

    :return:
    """
    public_instance = args[0]  # type:PublicAccount
    action = get_params(request, name='action')
    form = MaterialMediaForm()
    action = get_params(request, name='action')
    if action == 'edit':
        error_msg = u'素材暂不允许你编辑，请删除后再添加'
        return render(request, "error/error.html", locals())
    if request.method == 'POST':
        form = MaterialMediaForm(data=request.POST, files=request.FILES, instance=MediaModel(public=public_instance))
        if form.is_valid():
            # todo 从内存直接生成string io file object
            form.save()

            form.instance.media_id = public.upload_media(form.instance.type, form.instance.file.file.file)['media_id']
            form.save()
            return render(request, 'error/success.html', locals())
    if action == 'add':
        form_method = 'post'
        return render(request, 'base/form.html', locals())

    table_datas = all_medias = MediaModel.objects.filter(public=public_instance)

    return render(request, 'wechat_manage/material_display.html', locals())
