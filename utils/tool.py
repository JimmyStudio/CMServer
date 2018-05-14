# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         tool.py
time:         2018/5/4 下午12:58
description: 

'''

__author__ = 'Jimmy'

import datetime as dt

def conver_sec(sec):
    h = int(sec / 3600)
    m_left = sec % 3600
    m = int(m_left/60)
    s_left = m_left % 60
    if h == 0:
        return str(m).zfill(2) +':' + str(s_left).zfill(2)
    else:
        return str(h).zfill(2)+':'+str(m).zfill(2) +':' + str(s_left).zfill(2)


def getTime():
    nowTime = str(dt.datetime.now()).split('.')[0]
    part = nowTime.split(' ')
    part1 = part[0].split('-')
    part2 = part[1].split(':')
    ret = [int(part1[0]), int(part1[1]), int(part1[2]),int(part2[0]), int(part2[1]), int(part2[2])]
    return ret


if __name__ == "__main__":
    print(getTime())