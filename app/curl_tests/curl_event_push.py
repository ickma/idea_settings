# coding:utf8
# @author:nick
# @company:joyme
import os
import time

timestamp = int(time.time())
# openid
user_openid = 'oSRd6wKyAzQqDGhd8EPrWSVivTxE' #machao198205
# user_openid = 'oSRd6wNKMCcUm_857hnvR5aTg0ic'
# 公众号 token
public_token = 'iyFMiQOKCTR7l8BKZCft'


class EventPush(object):
    xml_raw = r"""
    <xml>
<ToUserName><![CDATA[{token}]]></ToUserName>
<FromUserName><![CDATA[{openid}]]></FromUserName>
<CreateTime>{timestamp}</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[{event_type}]]></Event>
<EventKey><![CDATA[{event_key}]]></EventKey>
</xml>
    """

    def __init__(self):
        self.xml = self.xml_raw.format(event_type="CLICK", event_key='Test', timestamp=timestamp, token=public_token,
                                       openid=user_openid)
        super(EventPush, self).__init__()

    def __str__(self):
        return self.xml

    def get_xml(self):
        return self.xml


class EventPushProxy(object):
    _class = ''

    def __init__(self, event_name=''):
        if event_name == '':
            self._class = EventPush()
        super(EventPushProxy, self).__init__()

    def register(self, class_name):
        pass

    def push(self):
        testing_url = 'http://127.0.0.1:8001/public/1'
        os.system('curl -d "%s" %s' % (self._class.get_xml(), testing_url))


EventPushProxy().push()
