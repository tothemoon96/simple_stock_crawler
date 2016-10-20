# -*- coding: utf-8 -*-
import logging
from sqlalchemy import Column, DateTime, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.attributes import InstrumentedAttribute
from stock_price_crawler.database import InitDB, DBSession

logger = logging.getLogger(__name__)


class ItemTable(InitDB.Base):
    '''
        表item_table的持久化对象
    '''
    __tablename__ = 'item_table'
    stock_market = Column('stock_market', String(255), primary_key=True)
    stock_market_link = Column('stock_market_link', String(255))
    scrape_time = Column('scrape_time', DateTime())

    def __init__(self, stock_market, stock_market_link, scrape_time, database):
        self.stock_market = stock_market
        self.stock_market_link = stock_market_link
        self.scrape_time = scrape_time
        self.database = database

    def __repr__(self):
        return (
            u"<ItemTable(stock_market='{0}',"
            u"stock_market_link='{1}',"
            u"scrape_time=='{2}')>"
        ).format(
            self.stock_market,
            self.stock_market_link,
            self.scrape_time
        )

    def insert(self):
        '''
        插入数据，如果数据存在就更新
        :return:
        '''
        with DBSession(self.database.Session) as session:
            try:
                session.add(self)
                session.flush()
            except IntegrityError, e:
                logger.info(e.message)
                # 如果该主键值已经存在，就更新该数据
                if 'Duplicate' in e.message:
                    session.rollback()
                    logger.info('Records exists')
                    self.update()
                # 如果是其他的问题，就把异常继续向上抛
                else:
                    raise e

    def update(self):
        '''
        用当前的对象更新数据
        :return:
        '''
        with DBSession(self.database.Session) as session:
            mapped_values = {}
            for field_name, field_type in ItemTable.__dict__.iteritems():
                if isinstance(field_type, InstrumentedAttribute):
                    mapped_values[field_name] = getattr(self, field_name)
            session.query(ItemTable).filter(
                ItemTable.stock_market == self.stock_market
            ).update(mapped_values)
