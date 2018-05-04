# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         tool.py
time:         2018/5/4 下午12:58
description: 

'''

__author__ = 'Jimmy'

def conver_sec(sec):
    h = int(sec / 3600)
    m_left = sec % 3600
    m = int(m_left/60)
    s_left = m_left % 60
    if h == 0:
        return str(m).zfill(2) +':' + str(s_left).zfill(2)
    else:
        return str(h).zfill(2)+':'+str(m).zfill(2) +':' + str(s_left).zfill(2)
