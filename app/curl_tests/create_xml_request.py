# coding:utf8
# @author:nick
# @company:joyme
import time
import os
import random
import string

# openid
user_openid = 'oSRd6wKyAzQqDGhd8EPrWSVivTxE'
# 公众号 token
public_token = 'iyFMiQOKCTR7l8BKZCft'
# 测试文本消息sample
text = 'local test'
# 当前timestamp
timestamp = int(time.time())
# 测试图片消息sample
image_url = 'https://img11.360buyimg.com/cms/jfs/t3703/296/223334932/244921/9e3c5ae9/5803786dN96d3fe6d.jpg'
# 测试用msgid
random_msgid = random.randint(2 ** 10 + 1, 2 **60)
# 测试用mediaid
random_mediaid = ''.join([random.choice(string.letters) for n in range(32)])
text_msg = """<xml>
 <ToUserName><![CDATA[{0}]]></ToUserName>
 <FromUserName><![CDATA[{1}]]></FromUserName>
 <CreateTime>{3}</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[{2}]]></Content>
 <MsgId>{4}</MsgId>
 </xml>""".format(public_token, user_openid, text, timestamp,random_msgid)

image_msg = """
 <xml>
 <ToUserName><![CDATA[{token}]]></ToUserName>
 <FromUserName><![CDATA[{openid}]]></FromUserName>
 <CreateTime>{timestamp}</CreateTime>
 <MsgType><![CDATA[image]]></MsgType>
 <PicUrl><![CDATA[{imageurl}]]></PicUrl>
 <MediaId><![CDATA[{mediaid}]]></MediaId>
 <MsgId>{msgid}</MsgId>
 </xml>
""".format(openid=user_openid, token=public_token, timestamp=timestamp, imageurl=image_url, msgid=random_msgid,
           mediaid=random_mediaid)

random_mediaid='zjfTr8SkzCk8fuapmKwBNWoxL1dM9vTjAjSeDRTkhuWh0zBASKHs2F01Qz59oWsK'
voice_msg = """
<xml>
<ToUserName><![CDATA[{token}]]></ToUserName>
<FromUserName><![CDATA[{openid}]]></FromUserName>
<CreateTime>{timestamp}</CreateTime>
<MsgType><![CDATA[voice]]></MsgType>
<MediaId><![CDATA[{mediaid}]]></MediaId>
<Format><![CDATA[amr]]></Format>
<MsgId>{msgid}</MsgId>
</xml>
""".format(openid=user_openid, token=public_token, timestamp=timestamp, mediaid=random_mediaid, msgid=random_msgid)

video_msg = """
<xml>
<ToUserName><![CDATA[{token}]]></ToUserName>
<FromUserName><![CDATA[{openid}]]></FromUserName>
<CreateTime>{timestamp}</CreateTime>
<MsgType><![CDATA[video]]></MsgType>
<MediaId><![CDATA[{mediaid}]]></MediaId>
<ThumbMediaId><![CDATA[{mediaid}]]></ThumbMediaId>
<MsgId>{msgid}</MsgId>
</xml>
""".format(token=public_token, openid=user_openid, timestamp=timestamp, mediaid=random_mediaid, msgid=random_msgid)

event_msg = """
<xml>
<ToUserName><![CDATA[{toekn}]]></ToUserName>
<FromUserName><![CDATA[{openid}]]></FromUserName>
<CreateTime>{timestamp}</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[CLICK]]></Event>
<EventKey><![CDATA[HAHA]]></EventKey>
</xml>
""".format(toekn=public_token, openid=user_openid, timestamp=timestamp)

testing_url = os.environ['testing_url']
testing_type = os.environ['testing_type']
# 读取当前的测试类型
test_xml = text_msg
if testing_type == 'image':
    test_xml = image_msg
if testing_type == 'voice':
    test_xml = voice_msg
if testing_type == 'video':
    test_xml = video_msg
if testing_type == 'event':
    test_xml = event_msg

need_output = ''
try:
    if os.environ['testing_output'] == 'true':
        need_output = '-O'
except KeyError:
    pass

# 执行测试
os.system('curl -d "%s" %s %s' % (test_xml, testing_url, need_output))
