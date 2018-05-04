# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         dao.py
time:         2018/3/21 上午10:11
description: 

'''

__author__ = 'Jimmy'

from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, Integer, Text, Numeric, Boolean, Float
from sqlalchemy.orm import sessionmaker, relationship
import hashlib

engine = create_engine('mysql+mysqlconnector://root:846880@localhost:3306/cmdb?charset=utf8')
Base = declarative_base()

# price coin 均为整数 22位 18位整数+4位小数

# user - ip 多对多 版权占有额度
class Share(Base):

    __tablename__ = 'share'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    ip_id = Column(Integer)
    share = Column(Integer) # balance of token

# tag - IP 多对多
tag_ip = Table(
    'tag_ip', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('ip_id', Integer, ForeignKey('ip.id')),
)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True)
    password = Column(String(64))
    email = Column(String(64),index=True)
    phone = Column(String(64),index=True)
    eth_address = Column(String(256),index=True)  # eth address
    coin = Column(Integer) # balance of token
    ips = relationship('IP', backref = 'user')
    brief = Column(Text) # user brief
    token = Column(String(256)) # login token

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.eth_address)

# 市场
class Market(Base):

    __tablename__ = 'market'

    id = Column(Integer, primary_key=True)
    ip_id = Column(Integer, index=True)
    ip_type = Column(Integer, index=True) # 0 pic 1 music 2 video 3 doc
    manager_id = Column(Integer, index=True) # the person who put on market must have share of the ip
    price = Column(Integer) # price
    sell_type = Column(Integer, index=True) # 0 not available ; 1 for use ; 2 for copyrights

# 我喜欢的
class Like(Base):

    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)
    ip_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True) # 0 pic 1 music 2 video 3 doc


class IP(Base):

    __tablename__ = 'ip'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.id')) # the person who upload it
    ip_type = Column(Integer) # 0 pic 1 music 2 video 3 doc
    duration = Column(Integer) # duration of music or video
    name = Column(String(256)) # ip name
    desc = Column(Text) # ip description
    local_path = Column(String(256)) # local path in server
    cover_image_path = Column(String(256)) # local path in server of cover image
    feature_hash = Column(String(256)) # feature hash of the ip
    ipfs_hash = Column(String(256)) # ipfs location
    use_sell_count = Column(Integer) # sell count for self usage
    copyright_sell_count = Column(Integer) # sell count for copyright shares
    transactions = relationship('Transaction', backref = 'ip')
    tags = relationship("Tag", secondary=tag_ip,backref="ips") #=> 会在Tag中加一个ips属性 获取包含该tag的所有ip的list

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.ipfs_hash)

class Tag(Base):

    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(256)) # tag name

class Transaction(Base):

    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    ip_id = Column(Integer, ForeignKey('ip.id'))
    transac_type = Column(Integer) # 0 create  1 ip transaction 2 use transaction
    transac_hash = Column(String(256)) # eth transaction hash
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    hour = Column(Integer)
    minute = Column(Integer)
    sec = Column(Integer)
    from_user_id = Column(Integer)
    to_user_id = Column(Integer)


    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.ipfs_hash)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # pw = '123456'
    # hpw = hashlib.md5()
    # hpw.update(pw.encode(encoding='utf-8'))
    # password = hpw.hexdigest()
    #
    # tags = [Tag(name='孤单'), Tag(name='快乐'), Tag(name='沉重'), Tag(name='自然'), Tag(name='自由'), Tag(name='舒服'),Tag(name='活泼'),Tag(name='迷恋'), Tag(name='幸福'), Tag(name='喜爱'), Tag(name='感动'), Tag(name='轻松'),]
    # user = User(username='admin',password=password,phone='13818617241',email='234390130@qq.com',eth_address='0x298A7CEd882d922D49B5328397Be60C1FE9d4BDb',token=0)
    # ip1 = IP(ip_type=1, sender_id =1,name='片头曲', desc='片头曲测试片头曲测试片头曲测试', local_path='/static/9863.mp3', cover_image_path ='/static/images/1.jpg')
    # ip2 = IP(ip_type=1, sender_id =1,name='开场', desc='开场开场开场开场开场开场开场开场', local_path='/static/9711.mp3',  cover_image_path ='/static/images/2.jpg')
    # share1 = Share(user_id=1, ip_id=1,price=100,share=100)
    # share2 = Share(user_id=1, ip_id=2,price=200,share=100)
    # m1 = Market(ip_id=1, ip_type=1,manager_id=1,sell_type=1)
    # m2 = Market(ip_id=2, ip_type=1,manager_id=1,sell_type=1)
    # tags.append(user)
    # tags.append(ip1)
    # tags.append(ip2)
    # tags.append(share1)
    # tags.append(share2)
    # tags.append(m1)
    # tags.append(m2)

    # ip = session.query(IP).filter(IP.id == 1).one()
    # tags = session.query(Tag).filter(Tag.id < 4).all()
    # for tag in tags:
    #     ip.tags.append(tag)
    # session.flush()
    # # session.add_all(tags)
    # session.commit()
