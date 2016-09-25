# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class StockPriceCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 行业的名字
    stock_market = scrapy.Field(output_processor=TakeFirst())
    # 行业详细信息的网页地址
    stock_market_link = scrapy.Field(output_processor=TakeFirst())
