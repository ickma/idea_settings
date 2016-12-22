# coding:utf8
# @author:nick
# @company:joyme
import time
import hashlib
import random
import string
import os

url = 'http://127.0.0.1:8000/public/1'
token = 'iyFMiQOKCTR7l8BKZCft'
timestamp = str(int(time.time()))
echostr = ''.join([random.choice(string.letters) for n in range(20)])
nonce = str(random.randint(1000000, 100000000))
_ = ''.join(sorted([token, timestamp, nonce])).encode('utf-8')
s = hashlib.sha1(_).hexdigest()
public_url = url + '?timestamp=%s&nonce=%s&signature=%s&echostr=%s' % (timestamp, nonce, s, echostr)
# 执行curl
os.system('curl "%s"' % public_url)
