# -*- coding: utf-8 -*-
import logging
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from stock_price_crawler.database import InitDB, DBSession

logger = logging.getLogger(__name__)


class InstanceTable(InitDB.Base):
    '''
    表instance的持久化对象
    '''
    __tablename__ = 'instance'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    address = Column('address', String(255))
    name = Column('name', String(255))
    status = Column('status', String(255))
    module = Column('module', String(255))
    service = Column('service', String(255))

    _database = InitDB('config.yaml')

    def __repr__(self):
        return (
            u"<InstanceTable(id='{0}',"
            u"address='{1}',"
            u"name='{2}',"
            u"status='{3}',"
            u"module='{4}',"
            u"service='{5}')>"
        ).format(
            self.id,
            self.address,
            self.name,
            self.status,
            self.module,
            self.service
        )

    @classmethod
    def insert(cls, obj):
        '''
        插入数据
        :return:instance的id
        '''
        with DBSession(cls._database.Session) as session:
            session.add(obj)
            session.flush()
            id = obj.id
        return id

    @classmethod
    def update(cls, id, key, value):
        '''
        根据id更新对象
        '''
        with DBSession(cls._database.Session) as session:
            session.query(InstanceTable).filter(
                InstanceTable.id == id
            ).update({key: value})
