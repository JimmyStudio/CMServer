# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         test.py
time:         2018/3/16 下午7:20
description: 

'''

__author__ = 'Jimmy'

import requests
import json

r = requests.post('http://localhost:8888/uploadmywork',
                  {'token':'55a7dfc94a2c7bb872595d6936e1839e',
                    'local_path':'/asfd.mp3',
                    'name':'哈哈哈',
                    'bref':'测试测试测试',
                   'cover_image_path':'/dsad.jpg',
                    'price':100000
                   })

print(json.loads(r.text))
