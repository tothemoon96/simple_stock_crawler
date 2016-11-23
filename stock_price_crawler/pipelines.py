# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from stock_price_crawler.database import InitDB
from stock_price_crawler.models.data import ItemTable
from stock_price_crawler.time_util import get_current_time_with_local_time_zone


class StockPriceCrawlerPipeline(object):
    def process_item(self, item, spider):
        database = InitDB('config.yaml')
        current_time_string = \
            get_current_time_with_local_time_zone() \
            .strftime("%Y-%m-%d %H:%M:%S")
        data = ItemTable(
            stock_market=item['stock_market'],
            stock_market_link=item['stock_market_link'],
            scrape_time=current_time_string,
            database=database
        )
        data.insert_with_update()
        return item
