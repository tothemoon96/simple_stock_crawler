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
    '''
    这个类负责封装数据表的插入操作
    '''
    # 连接数据库驱动
    engine = create_engine_with()

    def __init__(self):
        '''
        初始化表的元信息
        '''
        self.table = Table(
            # 表名
            'item_table',
            MetaData(),
            # 板块名字
            Column('stock_market', String, primary_key=True),
            # 板块链接
            Column('stock_market_link', String),
            # 爬取时间
            Column('scrape_time', DateTime),
        )

    def insert(self, **kwargs):
        '''
        进行插入操作，如果stock_market和数据表里的重复，就更新这一行
        :param kwargs: 传入的包含数据的字典
        :return:
        '''
        try:
            # 进行插入操作
            with DBConnection(self.engine) as connection:
                connection.execute(self.table.insert().values(**kwargs))
        except IntegrityError, e1:
            # 如果是因为主键重复而插入失败，记录错误信息
            logger.info(e1.message)
            if 'Duplicate' in e1.message:
                logger.info('Records exist')
                stock_market = kwargs.pop('stock_market')
                # 进行更新
                update = self.table.update()\
                    .where(self.table.c.stock_market == stock_market)\
                    .values(**kwargs)
                try:
                    with DBConnection(self.engine) as connection:
                        connection.execute(update)
                    logger.info('Records update')
                # 更新的过程中如果出现了其他错误
                except BaseException, e2:
                    # 记录这个错误
                    logger.exception(e2)
            # 如果是其他原因引起插入失败
            else:
                # 记录这个失败原因
                logger.exception(e1)
