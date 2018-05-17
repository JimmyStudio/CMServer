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
import utils.etc as  etc
import datetime as dt

# import eyed3
# import os
#
# file_path = os.path.join('www/static/sounds', '10049.mp3')
# audiofile = eyed3.load(file_path)
# print(u'时长为：{}秒'.format(audiofile.info.time_secs))

r = requests.get('http://localhost:8888/blocks')
print(json.loads(r.text))