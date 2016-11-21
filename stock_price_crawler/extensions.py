# -*- coding: utf-8 -*-
import logging
import os
import socket
from scrapy import signals
from stock_price_crawler.models.crawler_stock_price_data \
    import CrawlerStockPriceDataTable
from stock_price_crawler.models.instance import InstanceTable

logger = logging.getLogger(__name__)


class StockPriceExtension(object):
    '''
    用于追踪爬虫动态的扩展
    '''

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        extension = cls(crawler.stats)
        crawler.signals.connect(
            extension.spider_opened,
            signal=signals.spider_opened
        )
        crawler.signals.connect(
            extension.spider_closed,
            signal=signals.spider_closed
        )
        return extension

    def spider_opened(self, spider):
        '''
        爬虫打开的时候，初始化记录项
        '''
        logger.info('Start logging crawler records')

    def spider_closed(self, spider, reason):
        '''

        :param spider:spider的对象
        :param reason:关闭原因
        :return:
        '''
        CrawlerStockPriceDataTable.insert(
            CrawlerStockPriceDataTable(
                instance_id=spider.instance_id,
                start_time=self.stats.get_value('start_time'),
                finish_time=self.stats.get_value('finish_time'),
                item_scraped_count=self.stats.get_value('item_scraped_count'),
                log_count_warning_count=self.stats.get_value(
                    'log_count/WARNING'
                )
            )
        )


class InstanceExtension(object):
    '''
    用于创建及追踪实例状态的扩展
    '''
    error_status = False

    @classmethod
    def from_crawler(cls, crawler):
        extension = cls()
        crawler.signals.connect(
            extension.spider_opened,
            signal=signals.spider_opened
        )
        crawler.signals.connect(
            extension.spider_closed,
            signal=signals.spider_closed
        )
        crawler.signals.connect(
            extension.spider_error,
            signal=signals.spider_error
        )
        return extension

    def spider_opened(self, spider):
        '''
        爬虫开启时，创建实例
        '''
        localIP = socket.gethostbyname(socket.gethostname())
        spider.instance_id = InstanceTable.insert(
            InstanceTable(
                address=localIP,
                name=os.environ['SCRAPY_JOB'],
                status='running',
                module='crawler',
                service='stock_price'
            )
        )

    def spider_closed(self, spider, reason):
        '''
        爬虫关闭时，关闭实例
        '''
        # 修改数据库中status的状态
        if reason == 'finished' and not self.error_status:
            InstanceTable.update(spider.instance_id, 'status', 'closed')
        else:
            InstanceTable.update(spider.instance_id, 'status', 'error')

    def spider_error(self, failure, response, spider):
        '''
        爬虫发生错误，修改实例状态
        '''
        # 修改数据库中status的状态
        InstanceTable.update(spider.instance_id, 'status', 'error')
        self.error_status = True
