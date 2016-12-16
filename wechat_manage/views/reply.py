# coding:utf8
# @author:nick
# @company:joyme

from . import HttpRequest, HttpResponse
from . import WechatBasic, WechatConf
from . import render, get_params
from . import catch_error, login_required, auth_public
from wechat_manage.models.reply_model import ReplyConfigModel
from wechat_manage.forms.reply_form import BaseReplyForm, KeyWorldReplyForm


@login_required
# @catch_error
@auth_public
def welcome_reply(request, public, *args):
    """
    :type request:HttpRequest
    :type public:WechatBasic
    :type args:[WechatBasic]
    :param request:
    :param public:
    :return:
    """

    public_instance = args[0]
    try:
        welcome_reply_instance = ReplyConfigModel.objects.get(public=public_instance,
                                                              reply_type=1)  # type:ReplyConfigModel,bool
    except ReplyConfigModel.DoesNotExist:
        welcome_reply_instance = ReplyConfigModel(public=public_instance, reply_type=1)
    initial_dict = {'content': welcome_reply_instance.content, 'file': welcome_reply_instance.file,
                    'content_type': welcome_reply_instance.content_type}

    if request.method == 'POST':
        welcome_reply_instance.content_type = get_params(request, method='post', name='content_type')
        welcome_reply_instance.content = get_params(request, method='post', name='content')
        welcome_reply_instance.file = request.FILES['file']
        welcome_reply_instance.save()
        return render(request, 'error/success.html', locals())
        # if file
    form_method = 'post'
    form = BaseReplyForm(initial=initial_dict)
    return render(request, 'wechat_manage/reply_base.html', locals())
