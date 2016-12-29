# coding:utf8
# @author:nick
# @company:joyme

from django.contrib.auth.decorators import login_required
from permissions.utils.decoraters import auth_public
from . import HttpRequest, WechatBasic, render
from . import get_params, catch_error
from . import ViewNotReady
from wechat_manage.models.followers_model import PublicFollowers
from wechat_manage.models.public_model import PublicAccount
from wechat_manage.utils.followers_utils import get_all_openids


@login_required
@catch_error
@auth_public
def user_index(request, public, *args):
    """
    :type request: HttpRequest
    :type public:WechatBasic
    :param request:
    :param public:
    :return:
    """
    public_instance = PublicAccount.objects.get(app_id=public.conf.appid)
    table_datas=datas = PublicFollowers.objects.all().filter(public=public_instance)
    page_title = u'粉丝首页'
    return render(request, 'followers/followers_table.html', locals())


@catch_error
@login_required
@auth_public
def sync_followers(request, public, *args, **kwargs):
    """
    同步粉丝信息
    :param request:
    :param public:
    :type public:WechatBasic
    :return:
    """
    page_title = u'同步用户'
    table_heads = table_datas = []
    # return render(request,'base/simple_table.html',locals())
    step = get_params(name='step', request=request, formatter=int, default=1)
    public_instance = PublicAccount.objects.get(app_id=public.conf.appid)
    # 拉取关注者列表
    if step == 1:
        openids = get_all_openids(public=public)

        for openid in openids:
            follower_instance, created = PublicFollowers.objects.get_or_create(openid=openid, public=public_instance)
            if not created:
                follower_instance.save()
        success_msg = u'拉取用户列表成功\n即将拉取用户基本信息'
        jump_url = '%s?step=2' % request.path
        # return render(request, "followers/followers_info.html", locals())
    # 逐条拉取用户详情
    if step == 2:
        once_total, total = 200, PublicFollowers.objects.count()
        start_index = get_params(request, name='index', default=0, formatter=int)
        openids = PublicFollowers.objects.all()[start_index:(start_index + once_total)]
        for openid in openids:
            follower_info = public.get_user_info(openid.openid)
            follower_instance = PublicFollowers.objects.get(openid=openid.openid, public=public_instance)
            for k, v in follower_info.items():
                setattr(follower_instance, k, v)
            follower_instance.save()
        success_msg = u'拉取用户信息成功\n已获取%s-%s位用户' % (start_index, start_index + len(openids))
        if start_index + once_total >= total:
            jump_url = 'end'
        else:
            jump_url = "'%s?step=2&index=%s" % (request.path, start_index + once_total)
    return render(request, 'followers/followers_info.html', locals())


@login_required
@catch_error
@auth_public
def followers_group(request, wechatsdk, *args):
    """
    用户分组
    :param request:
    :param wechatsdk:
    :type request: object
    :return:
    """
    # not ready
    raise ViewNotReady


@login_required
@catch_error
@auth_public
def followers_message(request, wechasdk, *args):
    raise ViewNotReady
    pass
