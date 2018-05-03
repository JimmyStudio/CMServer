# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         helper.py
time:         2018/5/3 下午5:38
description: 

'''

__author__ = 'Jimmy'

from database.dao import *
import json
import copy

Session = sessionmaker(bind=engine)
session = Session()

def get_hot_recommend(type=1):
    ips = session.query(Market).filter(Market.sell_type==type).limit(12).all()
    rets = []
    for ip in ips:
        ip_info = session.query(IP).filter(IP.id == ip.ip_id).first()
        tags = []
        for tag in ip_info.tags:
            tg = copy.deepcopy(tag.__dict__)
            del tg['_sa_instance_state']
            tags.append(tg)
        ret = copy.deepcopy(ip_info.__dict__)
        del ret['_sa_instance_state']
        user_info = session.query(User).filter(User.id == ip_info.sender_id).first()
        ret['author_name'] = user_info.username
        ret['tags'] = tags
        rets.append(ret)
    return json.dumps({'list': rets})


if __name__ == "__main__":
    ret = get_hot_recommend()
    print(json.dumps(ret))