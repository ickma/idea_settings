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
@catch_error
@auth_public
def welcome_reply(request, public, *args):
    """
    欢迎语设置
    默认回复设置
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
    initial_dict = {'reply_content': welcome_reply_instance.reply_content, 'file': welcome_reply_instance.file,
                    'content_type': welcome_reply_instance.content_type}

    if request.method == 'POST':
        welcome_reply_instance.content_type = get_params(request, method='post', name='content_type',formatter=int)
        welcome_reply_instance.content = get_params(request, method='post', name='content')
        if not welcome_reply_instance.file or request.FILES.get('file'):
            welcome_reply_instance.file = request.FILES.get('file')
        welcome_reply_instance.save()
        return render(request, 'error/success.html', locals())
        # if file
    form_method = 'post'
    form = BaseReplyForm(initial=initial_dict)
    return render(request, 'wechat_manage/reply_base.html', locals())


@login_required
@catch_error
@auth_public
def keywords_reply(request, public, *args):
    """
    关键字回复
    :param request:
    :param public:
    :param args:
    :return:
    """

    public_instance = args[0]
    reply_id = get_params(request, name='id', formatter=int, default=0)
    reply_instance = ReplyConfigModel(public=public_instance)
    if reply_id:
        reply_instance = ReplyConfigModel.objects.get(id=reply_id)
    action = get_params(request, name='action', default='')
    if request.method == 'POST':
        reply_instance.content = get_params(request, name='reply_content', method='post')
        reply_instance.content_type = get_params(request, name='content_type', method='post', formatter=int)
        if not reply_instance.file or request.FILES.get('file'):
            reply_instance.file = request.FILES.get('file')
        reply_instance.reply_type = 3
        reply_instance.name = get_params(request, name='name', method='post')
        reply_instance.keywords = get_params(request, name='keywords', method='post')
        reply_instance.save()
        success_msg = u'提交成功'
        return render(request, 'error/success.html', locals())
    form_method = 'post'
    if action:
        initial = {'name': reply_instance.name, 'reply_content': reply_instance.reply_content, 'file': reply_instance.file,
                   'content_type': reply_instance.content_type, 'keywords': reply_instance.keywords}

        form = KeyWorldReplyForm(initial=initial)
        return render(request, "wechat_manage/reply_base.html", locals())

    all_replies = ReplyConfigModel.objects.filter(reply_type=3, public=public_instance)

    return render(request, "wechat_manage/reply_keyword.html", locals())
