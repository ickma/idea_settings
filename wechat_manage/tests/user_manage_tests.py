# coding:utf8
# @author:nick
# @company:joyme

from django.test import TestCase
from . import appid, app_secret, public
from wechat_sdk import WechatBasic
from wechat_manage.utils.followers_utils import get_all_openids


class UserTestCase(TestCase):
    def setUp(self):
        super(UserTestCase, self).setUp()

    def test_get_all_followers(self):
        """
        测试wechat sdk框架的获取全部关注者方法
        :return:
        """
        users = public.get_followers()
        print users
        self.assertGreater(users['total'], 5)

    def test_get_user_info(self):
        """
        测试wechat sdk的获取用户基本信息的方法
        :return:
        """
        users = public.get_followers()
        for user in users['data']['openid']:
            user_info = public.get_user_info(user)
            print user_info
            self.assertIn('openid', user_info.keys())

    def test_get_all_openid(self):
        """
        测试自定义的获取openid 方法,
        10000 关注者以内test ok
        10000 关注者以上未测试

        :return:
        """
        openids = get_all_openids(public=public)
        total= public.get_followers()['total']
        print  openids
        self.assertEqual(len(openids), total)
