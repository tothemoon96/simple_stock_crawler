# -*- coding: utf-8 -*-
import logging
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.exc import IntegrityError
from stock_price_crawler.database import create_engine_with, DBConnection

logger = logging.getLogger(__name__)


class ItemTable(object):
    engine = create_engine_with()

    def __init__(self):
        self.table = Table(
            'item_table',
            MetaData(),
            Column('stock_market', String, primary_key=True),
            Column('stock_market_link', String),
            Column('scrape_time', DateTime),
        )

    def insert(self, **kwargs):
        try:
            with DBConnection(self.engine) as connection:
                connection.execute(self.table.insert().values(**kwargs))
        except IntegrityError, e1:
            logger.info(e1.message)
            if 'Duplicate' in e1.message:
                logger.info('Records exist')
                stock_market = kwargs.pop('stock_market')
                update = self.table.update()\
                    .where(self.table.c.stock_market == stock_market)\
                    .values(**kwargs)
                try:
                    with DBConnection(self.engine) as connection:
                        connection.execute(update)
                    logger.info('Records update')
                except BaseException, e2:
                    logger.exception(e2)
            else:
                logger.exception(e1)
