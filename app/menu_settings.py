# coding:utf8
# @author:nick
# @company:joyme

BASIC_CONFIG = \
    {'name': u'基础配置',
     'children': [
         {
             'name': u'菜单配置',
             'path': ''
         },
         {
             'name': u'欢迎语配置',
             'path': ''
         },
         {
             'name': u'关键词回复',
             'path': ''
         },

     ]

     }

USER_MANAGE_CONFIG = {
    'name': u'用户管理',
    'children': [
        {
            'name': u'聊天记录',
            'path': ''
        },
        {
            'name': u'所有用户',
            'path': ''
        },
        {
            'name': u'用户分组',
            'path': ''
        },

    ]
}

MATERIAL_MANAGE_CONFIG = {
    'name': u'素材管理',
    'children': [
        {
            'name': u'获取素材',
            'path': ''
        },

    ]
}

MENU_CONFIG = [BASIC_CONFIG, USER_MANAGE_CONFIG, MATERIAL_MANAGE_CONFIG]
