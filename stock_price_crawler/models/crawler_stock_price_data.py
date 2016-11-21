# -*- coding: utf-8 -*-
import logging
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from stock_price_crawler import database
from stock_price_crawler.database import InitDB, DBSession

logger = logging.getLogger(__name__)


class CrawlerStockPriceDataTable(InitDB.Base):
    '''
    表crawler_stock_price_data_table的持久化对象
    '''
    __tablename__ = 'crawler_stock_price_data'
    instance_id = Column('instance_id', Integer, primary_key=True)
    start_time = Column('start_time', DateTime)
    finish_time = Column('finish_time', DateTime)
    item_scraped_count = Column('item_scraped_count', Integer)
    log_count_warning_count = Column('log_count_warning_count', Integer)

    _database = database._database

    def __repr__(self):
        return (
            u"<instance_id(id='{0}',"
            u"start_time='{1}',"
            u"finish_time='{2}',"
            u"item_scraped_count='{3}',"
            u"log_count_warning_count='{4}')>"
        ).format(
            self.instance_id,
            self.start_time,
            self.finish_time,
            self.item_scraped_count,
            self.log_count_warning_count
        )

    @classmethod
    def insert(cls, obj):
        '''
        插入数据
        :return:instance的id
        '''
        with DBSession(cls._database.Session) as session:
            session.add(obj)
