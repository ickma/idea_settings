# coding:utf8
# @author:nick
# @company:joyme
from . import PublicFollowers, WechatBasic


def get_all_openids(public, start_open_id=None, current_index=0):
    """
    :param current_index:
    :type current_index:int
    :param start_open_id:
    :type public:WechatBasic
    :type start_open_id:str | None
    :param public:
    :return:
    """
    openids = public.get_followers(start_open_id)
    count = openids['count']
    total = openids['total']
    if total == count or current_index + count == total:
        return openids['data']['openid']
    else:
        return openids['data']['openid'] + get_all_openids(public, start_open_id=openids['next_openid'],
                                                             current_index=current_index + 10000)
