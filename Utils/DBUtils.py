# -*- coding: utf-8 -*-
import queue

from time import sleep
import pymysql

'''
自定义异常类：
数据库异常
'''
class DBException(Exception):
    def __init__(self,type,message):
        self.type = type
        self.message = message

'''
Mysql数据库连接池
'''
class MysqlConnectPool:

    def __init__(self,maxsize=10):
        self.queue = queue.Queue(maxsize=maxsize)
        self.maxsize = maxsize
        self.full_pool()

    '''
    返回一个数据库连接实例
    '''
    def create_coon(self):
        db_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1314', db='dada', charset='utf8')
        return db_conn

    '''
    初始化连接池
    '''
    def full_pool(self):
        for i in range(self.maxsize):
            self.queue.put(self.create_coon)

    '''
    返回一个连接实例。
    如果连接池为空,则等待5秒后重试。重试三次后失败
    '''
    def get_db_coon(self):
        for i in range(3):
            try:
                if self.queue.qsize() > 0:
                    return self.queue.get()
                else:
                    raise DBException(type="GET_DB_COON_ERROR",message="can not get a mysql coon")
            except DBException as e:
                print(e.message)
                sleep(5)
        raise DBException(type="GET_DB_COON_ERROR",message="can not get a mysql coon after three attempts")

    '''
    将数据库实例纳入连接池
    '''
    def close(self,db):
        if self.queue.qsize() < self.maxsize:
            self.queue.put(db)

mysql_coon_pool = MysqlConnectPool(maxsize=10)

# 测试用
if __name__=="__main__":
    mysql_coon_pool.get_db_coon()
    mysql_coon_pool.get_db_coon()

