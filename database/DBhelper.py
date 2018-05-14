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
from utils import tool
import eyed3
import os
import datetime as dt
import random

# file_path = os.path.join('www/static/sounds', '10049.mp3')
# audiofile = eyed3.load(file_path)
# print(u'时长为：{}秒'.format(audiofile.info.time_secs))

Session = sessionmaker(bind=engine)

# 001 用户名或密码错误
# 002 登录过期 token不存在
# 003 文件类型错误
# 004 手机号已注册
# 005 代币余额不足
# 006 重复购买
# 007 无法购买自己的作品

# 100 成功

def getUserInfo(token):
    user = checkToken(token)
    if user == '002':
        return json.dumps({'err': '002', 'message': '登录已过期！'})
    else:
        ret = copy.deepcopy(user.__dict__)
        del ret['_sa_instance_state']
        return json.dumps({'user':ret,'err':'100', 'message':'成功'})

def buyWork(token, ip_id, from_user_id, price):
    user = checkToken(token)
    if user == '002':
        return json.dumps({'err': '002', 'message': '登录已过期！'})
    else:
        if user.id == from_user_id :
            return json.dumps({'err': '007', 'message': '无法购买您自己发布的作品！'})
        else:
            if user.coin < price:
                return json.dumps({'err': '005', 'message': '代币余额不足！'})
            else:
                sessionx = Session()
                trans = sessionx.query(Transaction).filter(
                    and_(Transaction.ip_id == ip_id, Transaction.from_user_id == from_user_id,
                         Transaction.transac_type == 1, Transaction.to_user_id == user.id)).all()
                if len(trans) > 0:
                    return json.dumps({'err': '006', 'message': '请勿重复购买！'})
                else:
                    session1 = Session()
                    coin1 = user.coin - price
                    session1.query(User).filter(User.id == user.id).update({User.coin: coin1})
                    session1.commit()

                    session2 = Session()
                    user2 = session2.query(User).filter(User.id == from_user_id).first()
                    coin2 = user2.coin + price
                    session2.query(User).filter(User.id == from_user_id).update({User.coin: coin2})
                    session2.commit()

                    session = Session()
                    tm = tool.getTime()
                    transc = Transaction(
                        ip_id=ip_id,
                        transac_type=1,  # usage
                        year=tm[0],
                        month=tm[1],
                        day=tm[2],
                        hour=tm[3],
                        minute=tm[4],
                        sec=tm[5],
                        from_user_id=from_user_id,
                        to_user_id=user.id,
                        price=price
                    )
                    session.add(transc)
                    session.commit()
                    return json.dumps({'err': '100', 'message': '购买成功'})


def uploadWork(token, local_path, name, brief, cover_image_path, price, sell_type, ip_type=1):
    user = checkToken(token)
    if user == '002':
        return json.dumps({'err': '002', 'message': '登录已过期'})
    else:
        # generate duration
        fn = local_path.split('/')[-1]
        file_path = os.path.join('www/static/sounds', fn)
        audiofile = eyed3.load(file_path)
        duration = audiofile.info.time_secs
        # generate feature_hash
        hpw = hashlib.md5()
        feature = str(time.time()) + str(user.id) +local_path
        hpw.update(feature.encode(encoding='utf-8'))
        feature_hash = hpw.hexdigest()

        session = Session()
        ip = IP(ip_type=ip_type,
                duration=duration,
                sender_id =user.id,
                feature_hash=feature_hash,
                name=name,
                brief=brief,
                sell_type = sell_type,
                price = price,
                local_path=local_path,
                cover_image_path =cover_image_path)
        session.add(ip)
        session.commit()

        session2 = Session()
        new_ip = session.query(IP).filter(IP.feature_hash == feature_hash).first()
        tm = tool.getTime()
        transc = Transaction(
            ip_id = new_ip.id,
            transac_type = 0, # create
            year = tm[0],
            month = tm[1],
            day = tm[2],
            hour = tm[3],
            minute = tm[4],
            sec = tm[5],
            from_user_id = 0,
            to_user_id = 0,
            price = new_ip.price
        )
        session2.add(transc)
        session2.commit()

        award = random.randint(0, 20)
        coin = user.coin + award
        session3 = Session()
        session3.query(User).filter(User.id == user.id).update({User.coin: coin})
        session3.commit()
        return json.dumps({'err':'100', 'message':'成功', 'award': award})


def getMyWorks(token):
    user = checkToken(token)
    if user == '002':
        return json.dumps({'err':'002', 'message':'登录已过期'})
    else:
        sendlist = []
        session = Session()
        ips = session.query(IP).filter(IP.sender_id == user.id).all()
        for ip_info in ips:
            ret = copy.deepcopy(ip_info.__dict__)
            del ret['_sa_instance_state']
            ret['duration'] = tool.conver_sec(ret['duration'])
            # count usage transc
            use_sell_count = 0
            for transc in ip_info.transactions:
                if transc.transac_type == 1:
                    use_sell_count += 1
            ret['use_sell_count'] = use_sell_count
            tags = []
            for tag in ip_info.tags:
                tg = copy.deepcopy(tag.__dict__)
                del tg['_sa_instance_state']
                tags.append(tg)
            # 创建者信息
            ret['author_name'] = user.username
            ret['tags'] = tags
            sendlist.append(ret)
        buylist = []
        # session2 = Session()
        trans = session.query(Transaction).filter(and_(Transaction.transac_type == 1, Transaction.to_user_id == user.id)).all()
        temp = {}
        for transc in trans:
            ip_info = session.query(IP).filter(IP.id == transc.ip_id).first()
            if ip_info.feature_hash in temp.keys():
                break
            else:
                temp[ip_info.feature_hash] = True
                ret = copy.deepcopy(ip_info.__dict__)
                del ret['_sa_instance_state']
                ret['duration'] = tool.conver_sec(ret['duration'])
                # count usage transc
                use_sell_count = 0
                for transc in ip_info.transactions:
                    if transc.transac_type == 1:
                        use_sell_count += 1
                ret['use_sell_count'] = use_sell_count
                tags = []
                for tag in ip_info.tags:
                    tg = copy.deepcopy(tag.__dict__)
                    del tg['_sa_instance_state']
                    tags.append(tg)
                # 创建者信息
                user_info = session.query(User).filter(User.id == ip_info.sender_id).first()
                ret['author_name'] = user_info.username
                ret['tags'] = tags
                buylist.append(ret)

        return json.dumps({'err':'100', 'message':'成功', 'sendlist': sendlist, 'buylist':buylist})


def logout(token):
    session = Session()
    session.query(User).filter(User.token == token).update({User.token:''})
    session.commit()
    return json.dumps({'err':'100', 'message':'退出成功！'})


def register(phone, password):
    session = Session()
    users = session.query(User).filter(User.phone == phone).all()
    if len(users) == 1:
        return json.dumps({'err': '004', 'message': '手机号已注册!'})
    else:
        hpw = hashlib.md5()
        hpw.update(password.encode(encoding='utf-8'))
        pw = hpw.hexdigest()

        tk = str(time.time()) + phone + password
        hpw.update(tk.encode(encoding='utf-8'))
        token = hpw.hexdigest()

        username = '用户' + phone[:3] + '****' + phone[7:]
        eth_address = '0x298A7CEd882d922D49B5328397Be60C1FE9d4BDb'

        user = User(username=username,
                    phone=phone,
                    password=pw,
                    token=token,
                    brief='暂无简介',
                    eth_address=eth_address,
                    email = None,
                    coin = 0,
                    portrait_path = None
                    )
        session.add(user)
        session.commit()
        user_dict = copy.deepcopy(user.__dict__)
        del user_dict['_sa_instance_state']
        user_dict['err'] = '100'
        user_dict['message'] = '注册成功'
        return json.dumps(user_dict)


def login(phone, password):
    session = Session()
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
        # session.flush()
        user['err'] = '100'
        user['message'] = '登录成功！'
        session.commit()
        return json.dumps(user)
    else:
        return json.dumps({'err':'001', 'message':'用户名或密码错误!'})


def get_hot_recommend(token, limit=12,type=1):
    return get_sounds(token=token, limit=limit, type=type)


def get_soundmart(token, type=1):
    return get_sounds(token=token, limit=0, type=type)


# tools
def checkToken(token):
    session = Session()
    users = session.query(User).filter(User.token == token).all()
    if len(users) == 1:
        return users[0]
    else:
        return '002'


def get_sounds(token, limit=0, type=1):
    session = Session()
    if limit == 0:
        ips = session.query(IP).filter(IP.sell_type == type).all()
    else:
        ips = session.query(IP).filter(IP.sell_type == type).limit(limit).all()
    rets = []
    for ip_info in ips:
        ret = copy.deepcopy(ip_info.__dict__)
        del ret['_sa_instance_state']
        ret['duration'] = tool.conver_sec(ret['duration'])
        # count usage transc
        use_sell_count = 0
        for transc in ip_info.transactions:
            if transc.transac_type == 1:
                use_sell_count += 1
        ret['use_sell_count'] = use_sell_count
        tags = []

        # ip 标签
        for tag in ip_info.tags:
            tg = copy.deepcopy(tag.__dict__)
            del tg['_sa_instance_state']
            tags.append(tg)
        # 创建者信息
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
    return json.dumps({'list': rets, 'err': '100', 'message': '成功'})


if __name__ == "__main__":
    print(json.loads(getMyWorks('b0c5e35e3ac0d75fd520de00c801ad56')))
    # uploadWork(token='d52b43143faf70237fd59944862b2055',
    #            local_path='/static/sounds/9711.mp3',
    #            name='发生该地块',
    #            brief='的胜多负少',cover_image_path='/static/images/1.jpg',
    #            sell_type=1,
    #            price=1000)