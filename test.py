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


r = requests.post('http://localhost:8888/myworks',
                  {'token':'f8296619671d3fd56e0aa0d6fc7f33cb'})

print(json.loads(r.text))
