# -*- coding: utf-8 -*-

'''
api handlers

'''

__author__ = 'Jimmy'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
import json
import os
from database import DBhelper



# arg:
## token
class post_logout(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        token = self.get_argument('token')
        ret = DBhelper.logout(token)
        self.write(ret)
        self.finish()

# arg:
## phone
## password
class post_login(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        phone = self.get_argument('phone')
        pw = self.get_argument('password')
        ret = DBhelper.login(phone, pw)
        self.write(ret)
        self.finish()

# arg:
## token
class post_hot_recommends(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        token = self.get_argument('token')
        ret = DBhelper.get_hot_recommend(token)
        self.write(ret)
        self.finish()

class upload_handler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')

        file_metas = self.request.files["upload_image"]  # 获取上传文件信息 fromdata => upload_image
        for meta in file_metas:  # 循环文件信息
            file_name = meta['filename']  # 获取文件的名称
            file_path = os.path.join('www/static', file_name)
            with open(file_path, 'wb') as up:  # os拼接文件保存路径，以字节码模式打开
                up.write(meta['body'])

        ret = {'path': file_path}
        self.write(ret)
        self.finish()


if __name__ == '__main__':
    file_name = 'dsa.img'
    ps = os.path.join('www/static',file_name)
    print(ps)
