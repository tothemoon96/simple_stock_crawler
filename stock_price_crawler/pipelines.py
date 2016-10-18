# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

from stock_price_crawler.database import InitDB
from stock_price_crawler.models.data import ItemTable


class StockPriceCrawlerPipeline(object):
    def process_item(self, item, spider):
        database = InitDB('config.yaml')
        data = ItemTable(
            stock_market=item['stock_market'],
            stock_market_link=item['stock_market_link'],
            scrape_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            database=database
        )
        ItemTable.insert(data)
        return item
