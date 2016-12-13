# coding:utf8
# @author:nick
# @company:joyme

BASIC_CONFIG = \
    {'name': u'基础配置',
     'children': [
         {
             'name': u'菜单配置',
             'path': '/wechat/{0}/menu/create'
         },
         {
             'name': u'欢迎语配置',
             'path': '{0}'
         },
         {
             'name': u'关键词回复',
             'path': '{0}'
         },

     ]

     }

USER_MANAGE_CONFIG = {
    'name': u'用户管理',
    'children': [
{
            'name': u'同步用户',
            'path': '/wechat/{0}/followers/sync'
        },
        {
            'name': u'聊天记录',
            'path': '{0}'
        },
        {
            'name': u'所有用户',
            'path': '{0}'
        },
        {
            'name': u'用户分组',
            'path': '{0}'
        },

    ]
}

MATERIAL_MANAGE_CONFIG = {
    'name': u'素材管理',
    'children': [
        {
            'name': u'获取素材',
            'path': '{0}'
        },

    ]
}

MENU_CONFIG = [BASIC_CONFIG, USER_MANAGE_CONFIG, MATERIAL_MANAGE_CONFIG]
