# coding:utf8
# @author:nick
# @company:joyme

from wechat_sdk import WechatBasic
from django.test import TestCase
from wechat_manage.models.public_model import PublicAccount


class MenuTestCase(TestCase):
    def setUp(self):
        # public_instance = PublicAccount.objects.get(pk=1)
        appid='wx52b3385a662272bd'
        app_secret='0e3a5714527a0141970c76e697d80830'
        self.public = WechatBasic(appid=appid, appsecret=app_secret)
        super(MenuTestCase, self).setUp()

    def test_menu_create(self):
        menu_config = {
            "button": [
                {
                    "type": "click",
                    "name": "啪啪以啪啪",
                    "key": "V1001_TODAY_MUSIC"
                },
                {
                    "type": "click",
                    "name": "摩擦以摩擦",
                    "key": "V1001_TODAY_MUSIC"
                },
                {
                    "name": "菜单",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "搜索",
                            "url": "http://www.soso.com/"
                        },
                        {
                            "type": "view",
                            "name": "视频",
                            "url": "http://v.QQ.com/"
                        },
                        {
                            "type": "click",
                            "name": "赞一下我们",
                            "key": "V1001_GOOD"
                        }]
                }]
        }
        self.public.create_menu(menu_data=menu_config)

    def test_get_menu(self):
        import json
        menus = self.public.get_menu()
        print  menus
        self.assertIn('menu', menus.keys())
