# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         mongo.py
time:         2018/5/17 下午3:53
description: 

'''

__author__ = 'Jimmy'

import pymongo
from utils import contract
import time
import copy
client = pymongo.MongoClient(host='127.0.0.1', port=27017)
# db_auth = client.admin
# db_auth.authenticate("jimmy", "846880")
db = client.chain

def insert_block_info():
    bn = 0
    res = db.block.find().sort("number", pymongo.DESCENDING).limit(1)
    while True:
        try:
            bn = next(res)
        except StopIteration:
            break
    while True:
        if contract.block_number() >= bn:
            bi = contract.block_info(bn)
            info = copy.deepcopy(bi.__dict__)
            db.block.insert(info)
            for th in info['transactions']:
                th_info = contract.transaction_info(th)
                if th_info:
                    th_info_dic = copy.deepcopy(th_info.__dict__)
                    db.transaction.insert(th_info_dic)
            bn += 1
        time.sleep(15)


def get_block_info(hx):
    res = db.block.find({'hash':hx})
    while True:
        try:
            temp = next(res)
            del temp['_id']
        except StopIteration:
            break
    trans = []
    for th in temp['transactions']:
        trans_res = db.transaction.find({'hash': th})
        while True:
            try:
                tempx = next(trans_res)
                del tempx['_id']
                trans.append(tempx)
            except StopIteration:
                break
    temp['trans'] = trans
    return temp

def get_all_blocks_info():
    res = db.block.find().sort("number", pymongo.DESCENDING)
    list = []
    while True:
        try:
            temp = next(res)
            del temp['_id']
            list.append(temp)
        except StopIteration:
            break
    return list

if __name__ == "__main__":
    print(get_block_info('0x4ee9fecd5dd74f8cdd0fd4a43457845e5f992dfdd7428e2ab8735270c926e532'))