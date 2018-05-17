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
from database import mongo

# arg:
class get_blocks(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        lst = mongo.get_all_blocks_info()
        ret = json.dumps({'err': '100', 'message': '成功！', 'blocks':lst})
        self.write(ret)
        self.finish()
# arg:
## token
## ip_id
class post_like(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        token = self.get_argument('token')
        ipid = self.get_argument('ipid')
        ret = DBhelper.like(token, ipid)
        self.write(ret)
        self.finish()

# arg:
## token
class post_user_info(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        token = self.get_argument('token')
        ret = DBhelper.getUserInfo(token)
        self.write(ret)
        self.finish()

# arg:
## token
## ip_id
## form
## price
class post_buywork(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        token = self.get_argument('token')
        ip_id = self.get_argument('ipid')
        from_user_id = self.get_argument('fromuserid')
        price = self.get_argument('price')
        ret = DBhelper.buyWork(token, ip_id, from_user_id, price)
        self.write(ret)
        self.finish()

# arg:
## phone
## password
class post_register(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        phone = self.get_argument('phone')
        pw = self.get_argument('password')
        ret = DBhelper.register(phone, pw)
        self.write(ret)
        self.finish()


# arg:
## token
class post_soundmart(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        token = self.get_argument('token')
        ret = DBhelper.get_soundmart(token)
        self.write(ret)
        self.finish()

# arg:
## token, local_path, name, bref, cover_image_path, price sell_type
class post_upload_mywork(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        token = self.get_argument('token')
        local_path = self.get_argument('local_path')
        name = self.get_argument('name')
        bref = self.get_argument('brief')
        cover_image_path = self.get_argument('cover_image_path')
        price = self.get_argument('price')
        sell_type = self.get_argument('sell_type')
        ret = DBhelper.uploadWork(token, local_path, name, bref, cover_image_path, price, sell_type)
        self.write(ret)
        self.finish()

# arg:
## token
class post_myworks(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        token = self.get_argument('token')
        ret = DBhelper.getMyWorks(token)
        self.write(ret)
        self.finish()

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
        file_metas = self.request.files["upload_file"]  # 获取上传文件信息 fromdata => upload_image
        for meta in file_metas:  # 循环文件信息
            file_name = meta['filename']  # 获取文件的名称
            # print(meta['content_type'])
            if meta['content_type'] == 'image/jpeg':
                file_path = os.path.join('www/static/images', file_name)
            elif meta['content_type'] == 'audio/mp3':
                file_path = os.path.join('www/static/sounds', file_name)
            else:
                file_path = ''
                break
            with open(file_path, 'wb') as up:  # os拼接文件保存路径，以字节码模式打开
                up.write(meta['body'])
        if file_path :
            file_path = file_path[3:]
            ret = {'path': file_path, 'err': '100', 'message': '成功'}
        else:
            ret = {'err': '003', 'message': '文件类型错误'}
        self.write(ret)
        self.finish()

if __name__ == '__main__':
    file_name = 'dsa.img'
    ps = os.path.join('www/static',file_name)
    print(ps)
