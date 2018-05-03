# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         ipfs.py
time:         2018/3/20 上午9:49
description: 

'''

__author__ = 'Jimmy'
import ipfsapi
api = ipfsapi.connect('127.0.0.1', 5001)
res = api.add('test.txt')
print(res)