# coding=utf-8
# @author:nick
# @company:joyme

BASIC_CONFIG = \
    {'name': u'基础配置',
     'children': [
         {
             'name': u'欢迎语配置',
             'path': '/wechat/{0}/reply/welcome'
         },
         {
             'name': u'关键词回复',
             'path': '/wechat/{0}/reply/keyword'
         },
         {
             'name': u'默认回复',
             'path': '/wechat/{0}/reply/default'
         },

     ]

     }

MENU_MANEGE_CONFIG = {
    'name': u'菜单配置',
    'children': [
        {
            'name': u'拉取菜单',
            'path': '/wechat/{0}/menu/sync'
        },
        {
            'name': u'编辑菜单',
            'path': '/wechat/{0}/menu/display'
        },

        {
            'name': u'推送菜单',
            'path': '/wechat/{0}/menu/push'
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
            'path': '/wechat/{0}/messages/display'
        },
        {
            'name': u'所有用户',
            'path': '/wechat/{0}/followers/query'
        },
        {
            'name': u'用户分组',
            'path': '/wechat/{0}/followers/group'
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
        {
            'name': u'多媒体素材管理',
            'path': '/wechat/{0}/material/manage'
        }

    ]
}

FEATHER_MANAGE_CONFIG = {
    'name': u'功能管理',
    'children': [
        {
            'name': u'礼包管理',
            'path': '/app/{0}/present/index'
        }
    ]
}

MENU_CONFIG = [BASIC_CONFIG, MENU_MANEGE_CONFIG, USER_MANAGE_CONFIG, MATERIAL_MANAGE_CONFIG, FEATHER_MANAGE_CONFIG]
