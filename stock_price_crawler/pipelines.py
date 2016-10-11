# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

from stock_price_crawler.models.data import ItemTable


class StockPriceCrawlerPipeline(object):
    def process_item(self, item, spider):
        '''
        将item保存进数据库
        :param item: 传入的要保存进数据库的item
        :param spider:爬虫上下文
        :return:item留作之后的处理
        '''
        # 将item转换成data字典，并添加爬取的时间
        data = dict()
        data['stock_market'] = item['stock_market']
        data['stock_market_link'] = item['stock_market_link']
        data['scrape_time'] = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime()
        )
        table = ItemTable()
        # 存入数据库
        table.insert(**data)
        return item
