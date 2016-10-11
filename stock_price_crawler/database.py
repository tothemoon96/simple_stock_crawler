# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from stock_price_crawler.config import Config


Settings = Config('config.yml').mysql


def create_engine_with(
        user=Settings.user,
        password=Settings.password,
        host=Settings.host,
        port=Settings.port,
        database=Settings.database
):
    '''

    :param user:用户名
    :param password:密码
    :param host:主机名
    :param port:端口号
    :param database:数据库名字
    :return:
    '''
    engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'
                           .format(user, password, host, port, database))
    return engine


class DBConnection(object):
    '''
    将数据库连接的事务处理包装进with...as...语句块
    '''
    def __init__(self, engine):
        self._engine = engine

    def __enter__(self):
        self._connection = self._engine.connect()
        self._trans = self._connection.begin()
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._trans.commit()
            self._connection.close()
            return True
        else:
            self._trans.rollback()
            self._connection.close()
            return False
