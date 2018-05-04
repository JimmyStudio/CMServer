# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         DBhelper.py
time:         2018/5/3 下午5:38
description: 

'''

__author__ = 'Jimmy'

from database.DAO import *
import json
import copy
from sqlalchemy import and_
import time
Session = sessionmaker(bind=engine)
session = Session()

# 001 用户名或密码错误
# 002 登录过期 token不存在

# 100 成功

def logout(token):
    users = session.query(User).filter(User.token == token).all()
    if len(users) == 1:
        # clear token
        session.query(User).filter(User.token == token).update({User.token:''})
        session.flush()
        session.commit()
        return json.dumps({'err':'100', 'message':'成功'})
    else:
        return json.dumps({'err':'002', 'message':'登录已过期'})


def login(phone, password):
    hpw = hashlib.md5()
    hpw.update(password.encode(encoding='utf-8'))
    pw = hpw.hexdigest()
    users = session.query(User).filter(and_(User.phone == phone, User.password == pw)).all()
    if len(users) == 1:
        user = copy.deepcopy(users[0].__dict__)
        del user['_sa_instance_state']
        tk = str(time.time())+phone+password
        hpw.update(tk.encode(encoding='utf-8'))
        token = hpw.hexdigest()
        user['token']= token
        session.query(User).filter(and_(User.phone == phone, User.password == pw)).update({User.token:token})
        session.flush()
        session.commit()
        return json.dumps(user)
    else:
        return json.dumps({'err':'001', 'message':'用户名或密码错误!'})


def get_hot_recommend(token,limit=12,type=1):
    ips = session.query(Market).filter(Market.sell_type==type).limit(limit).all()
    rets = []
    for ip in ips:
        ip_info = session.query(IP).filter(IP.id == ip.ip_id).first()
        tags = []
        # ip 标签
        for tag in ip_info.tags:
            tg = copy.deepcopy(tag.__dict__)
            del tg['_sa_instance_state']
            tags.append(tg)
        ret = copy.deepcopy(ip_info.__dict__)
        del ret['_sa_instance_state']
        # 用户信息
        user_info = session.query(User).filter(User.id == ip_info.sender_id).first()
        ret['author_name'] = user_info.username
        ret['tags'] = tags
        # 是否收藏
        users = session.query(User).filter(User.token == token).all()
        if len(users) == 1:
            user = users[0]
            like_info = session.query(Like).filter(and_(Like.user_id == user.id, Like.ip_id == ip_info.id)).all()
            if len(like_info) == 0:
                ret['like'] = False
            else:
                ret['like'] = True
        else:
            ret['like'] = False
        rets.append(ret)
    return json.dumps({'list': rets})


if __name__ == "__main__":
    print(get_hot_recommend('5d69fdcf8e9517617d035070adb48948'))