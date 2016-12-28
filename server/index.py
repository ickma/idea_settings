# coding:utf8
# @author:nick
# @company:joyme
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from django_wx_joyme.wsgi import application

container = WSGIContainer(application)
server = HTTPServer(container)
server.listen(8081)
# server.start(0)
IOLoop.current().start()
print  'app is listening at 8888'
