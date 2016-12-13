# coding:utf8
# @author:nick
# @company:joyme

from django.contrib.auth.decorators import login_required
from permissions.utils.decoraters import auth_public
from . import HttpRequest, HttpResponse, WechatBasic,render
from . import get_params,catch_error
from wechat_manage.models.followers_model import PublicFollowers
from wechat_manage.utils.followers_utils import get_all_openids


@login_required
@auth_public
@catch_error
def user_index(request, public):
    """
    :type request: HttpRequest
    :type public:WechatBasic
    :param request:
    :param public:
    :return:
    """
    all_followers = PublicFollowers.objects.all()

    pass


@login_required
@catch_error
@auth_public
def sync_followers(request, public):
    page_title=u'同步用户'
    table_heads=table_datas=[]
    # return render(request,'base/simple_table.html',locals())
    step = get_params(name='step', request=request, formatter=int)
    if step == 1:
        openids = get_all_openids(public=public)
        for openid in openids:
            follower_instance, created = PublicFollowers.objects.get_or_create(openid=openid, public=public)
            if not created:
                follower_instance.save()
        return
    start_index = get_params()
    pass
