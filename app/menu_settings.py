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
            'name': u'同步菜单',
            'path': '/wechat/{0}/menu/sync'
        },
        {
            'name': u'显示菜单',
            'path': '/wechat/{0}/menu/display'
        },
        {
            'name': u'菜单编辑',
            'path': '/wechat/{0}/menu/edit'
        },
        {
            'name': u'菜单增加',
            'path': '/wechat/{0}/menu/add'
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
            'path': '/wechat/{0}/followers/query'
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
            'path': '{0}'
        }
    ]
}

MENU_CONFIG = [BASIC_CONFIG, MENU_MANEGE_CONFIG, USER_MANAGE_CONFIG, MATERIAL_MANAGE_CONFIG,FEATHER_MANAGE_CONFIG]
