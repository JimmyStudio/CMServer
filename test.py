# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         test.py
time:         2018/3/16 下午7:20
description: 

'''

__author__ = 'Jimmy'

import os
import re
import sys
import eyed3


# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         # print('please input MP3 directory')
#         exit()
#
#     patemplate=r'\.mp3'
#     repat=re.compile(patemplate)
#
#     dir = sys.argv[1]
#     for filename in os.listdir(dir):
#         filepath = os.path.join(dir, filename)
#         p = re.compile(r'(.*)-(.*)\.mp3', re.I)
#         m = p.match(filename)
#         if m:
#             id3=filename
#             id3 = repat.sub('', filename)
#             audiofile = eyed3.load(filepath)
#             audiofile.initTag()
#             audiofile.tag.title = unicode(id3)
#             audiofile.tag.artist = u"NCE2"
#             audiofile.tag.album = u"NCE2"
#             audiofile.tag.album_artist = u"NCE2"
#             audiofile.tag.track_num = 0
#             audiofile.tag.comment=u"NCE2"
#             audiofile.tag.save()
#         else:
#             pass

import requests
import json
import utils.etc as  etc

import eyed3
import os

file_path = os.path.join('www/static/sounds', '10049.mp3')
audiofile = eyed3.load(file_path)
print(u'时长为：{}秒'.format(audiofile.info.time_secs))

# r = requests.post('http://localhost:8888/uploadmywork',
#                   {'token':'55a7dfc94a2c7bb872595d6936e1839e',
#                     'local_path':'/asfd.mp3',
#                     'name':'哈哈哈',
#                     'bref':'测试测试测试',
#                    'cover_image_path':'/dsad.jpg',
#                     'price':100000
#                    })
#
# print(json.loads(r.text))
