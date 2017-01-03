# coding:utf8
#  @author:nick
# @company:joyme
from django.shortcuts import render
from wechat_sdk.messages import WechatMessage
from wechat_manage.models.public_model import PublicAccount
from wechat_sdk import WechatBasic
from . import login_required, catch_error, auth_public, get_params
from . import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.models.message import Message, MsgResponse
from wechat_manage.models.followers_model import PublicFollowers
from app.messages.reply import Reply


@login_required
@catch_error
def index(request):
    """

    :param request:
    :return:
    """
    public_index = [('id', 'id'), ('public_name', u'名称'), ('public_type', u'公众号类别'), \
                    ('create_time', u'创建时间'), ('token', 'toekn'), ('api_url', u'接口地址'), ('public_manage', u'进入公众号')]
    page_title = u'微信管理:后台首页'
    table_title = u'选择公众号'
    # 获取公众号信息
    publics = PublicAccount.objects.all()

    table_heads = [x[1] for x in public_index]
    table_datas = []
    for public in publics:
        public.public_manage = '<a href="/wechat/%s/followers/query">进入管理</a>' % public.id
        public.api_url = 'http://%s/public/%d' % (request.get_host(), public.id)
        line = [getattr(public, key[0]) for key in public_index]

        table_datas += [line]
    return render(request, 'index/index_page.html', locals())


@csrf_exempt
@auth_public
def reply(request, public, *args):
    """
    作为 接口的view
    实现获取request并做出响应
    :type public: WechatBasic
    :param request:
    :param public:
    :param args:
    :return:
    """
    # 判断是否为微信的验证url请求
    signature = get_params(request, name='signature')
    echostr = get_params(request, name='echostr', default=None)
    if echostr:
        # 微信服务器验证url有效性逻辑
        nonce = get_params(request, name='nonce')
        timestamp = get_params(request, name='timestamp')
        if public.check_signature(signature, timestamp, nonce):
            return HttpResponse(echostr)
    # 获取微信公众号配置实例
    public_instance = args[0]
    # xml_string=request.body
    # from lxml import etree
    # xml=etree.fromstring(xml_string)

    # 使用sdk解析微信服务器发来的消息
    # sdk解析后将消息保存到实例中
    public.parse_data(request.body)
    # 从实例获取解析后的xml
    msg = public.get_message()
    """:type msg:WechatMessage"""
    try:
        user_instance = PublicFollowers.objects.get(public=public_instance, openid=msg.source)
    except PublicFollowers.DoesNotExist:
        user_instance = public.get_user_info(user_id=msg.source)
        """:type:dict"""
        # todo 实例化当前用户,待测试
        _user_instance = PublicFollowers(public=public_instance)
        for k, v in user_instance.items():
            setattr(_user_instance, k, v)
        _user_instance.save()
    """实例化message"""
    message_instance = Message(public=public_instance, form_user=user_instance, xml=request.body)

    message_instance.msg_instance = msg
    # 保存当前请求
    message_instance.save()
    # 回复逻辑
    reply_instance = Reply(message_instance=message_instance, wechatsdk_instance=public,
                           public_instance=public_instance)
    response = reply_instance.reply()
    """保存回复的response 实例"""
    message_instance.response = reply_instance.messages_response_instance
    message_instance.save()
    return HttpResponse(content=response)
