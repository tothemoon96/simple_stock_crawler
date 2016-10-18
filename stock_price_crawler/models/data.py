# -*- coding: utf-8 -*-
import logging
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
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

    def insert(self):
        with DBSession(self.database.Session) as session:
            try:
                session.add(self)
                session.flush()
            except IntegrityError, e:
                session.rollback()
                logger.info(e.message)
                # 如果该主键值已经存在，就更新该数据
                if 'Duplicate' in e.message:
                    logger.info('Records exists')
                    record = session.query(ItemTable).filter(
                        ItemTable.stock_market == self.stock_market
                    ).one()
                    session.delete(record)
                    session.add(self)
                    session.flush()
                else:
                    raise
