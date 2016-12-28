# coding=utf-8
"""django_wx_joyme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from django.templatetags.static import static

from wechat_manage.urls import urlpatterns as wechat_manage_urls
from app.views import index
from permissions.views import user_profile
from django.conf import settings
from django.conf.urls.static import static
from app.views.index import reply
from app.views.messages import messages

urlpatterns = [
                  url(r'^$', index.index),
                  url(r'^wechat/(?P<publicid>\d+)/messages/display', messages, name=u'查看用户聊天'),
                  url(r'^public/(?P<publicid>\d+)', reply, name=u'公众号对外接口'),  # 公众号向微信服务器提供的唯一接口
                  url(r'^admin/', admin.site.urls),
                  # set login url
                  url(r'^accounts/login/$', login, {'template_name': 'log/login.html'}, name='login'),
                  url(r'^user/profile$', user_profile, name=u'用户资料'),
                  #     set logout url
                  url(r'^signout', logout_then_login, name='signout'),
                  url(r'^wechat/(?P<publicid>\d+)', include(wechat_manage_urls))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
