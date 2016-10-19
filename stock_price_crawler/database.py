# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from stock_price_crawler.config import Config


class InitDB(object):
    '''
    封装engine和session实现单例模式
    '''
    Base = declarative_base()

    def __init__(self, config_file_name):
        self.engine = self.__create_engine_with(config_file_name)
        self.Session = sessionmaker(bind=self.engine)

    def __new__(cls, *args, **kw):
        '''
        \实现单例模式
        :param args:
        :param kw:
        :return:
        '''
        if not hasattr(cls, '_instance'):
            orig = super(InitDB, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def __create_engine_with(self, config_file_name):
        '''
        读取外部配置文件创建数据库引擎
        :param config_file_name:配置文件的名字
        :return:
        '''
        Settings = Config(config_file_name).mysql
        engine = create_engine(
            'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                .format(
                Settings.user,
                Settings.password,
                Settings.host,
                Settings.port,
                Settings.database
            )
        )
        return engine


class DBSession(object):
    '''
        封装Session类为更友好的with模式
    '''

    def __init__(self, Session):
        self.session = Session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
            self.session.close()
            return True
        else:
            self.session.rollback()
            self.session.close()
            return False
