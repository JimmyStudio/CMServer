# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         server.py
time:         2018/3/16 下午4:11
description: 

'''

__author__ = 'Jimmy'


import os.path
import tornado
from tornado.options import define, options
from apiHandlers import handlers
from tornado import httpserver

define("port", default=8888, help="run on the given port", type=int)

if __name__ == "__main__":
    print('start server at: localhost:%s' % options.port)

    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/myworks", handlers.post_myworks),
            (r"/login", handlers.post_login),
            (r"/logout", handlers.post_logout),
            (r"/recommend", handlers.post_hot_recommends),
            (r"/upload", handlers.upload_handler),
            (r"/uploadmywork", handlers.post_upload_mywork),
            (r"/soundmart", handlers.post_soundmart),
            (r"/register", handlers.post_register),
            (r"/buysound", handlers.post_buywork),
            (r"/userinfo", handlers.post_user_info),
            (r"/like", handlers.post_like),
            (r"/blocks", handlers.get_blocks),
            (r"/blockinfo", handlers.post_block_info),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "www"),
        static_path=os.path.join(os.path.dirname(__file__), "www/static")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


