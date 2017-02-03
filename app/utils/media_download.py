# coding:utf-8
# author:nick
# time:17-1-8

from wechat_sdk import WechatBasic
from app.models.message import Message, Media
from django_rq import job
from django.conf import settings
import re
import os


def download_media(wechatsdk, message_instance):
    """
    :type wechatsdk:WechatBasic
    :type message_instance:Message
    :param wechatsdk:
    :param message_instance:
    :return:
    """
    # 下载文件
    response = wechatsdk.download_media(media_id=message_instance.mediaid)
    d = response.headers['content-disposition']
    fname = re.findall("filename=\"(.+)\"", d)[0]
    file_path=os.path.join(settings.BASE_DIR, 'download', fname)
    with open(file_path, 'wb') as f:
        f.write(response.content)


    # 转码 amr文件
    if fname.split('.')[-1] == 'amr':

        os.system('yes |ffmpeg -i  %s %s '%(file_path,file_path[:-3]+'mp3'))
        fname = fname.replace('.amr', '.mp3')
    media_instance = Media(media_id=message_instance.mediaid, media_download_path=os.path.join('download', fname))
    media_instance.save()
    # message_instance=Message.objects.get(pk=message_instance.id)
    message_instance.media=media_instance
    message_instance.save(force_update=True)

