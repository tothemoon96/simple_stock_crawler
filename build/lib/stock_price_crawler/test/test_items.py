# -*- coding: utf-8 -*-
from nose.tools import assert_equals
from scrapy.loader import ItemLoader
from stock_price_crawler.items import StockPriceCrawlerItem


def test_StockPriceCrawlerItem():
    '''
    测试item的output_processor=TakeFirst()是否生效
    :return: None
    '''
    # 构造仿冒的测试数据
    fake_data = [
        {'stock_market': 'test1', 'stock_market_link': 'test1'},
        {'stock_market': 'test2', 'stock_market_link': 'test2'}
    ]
    loader = ItemLoader(item=StockPriceCrawlerItem())
    loader.add_value('stock_market', fake_data[0]['stock_market'])
    loader.add_value('stock_market', fake_data[1]['stock_market'])
    loader.add_value('stock_market_link', fake_data[0]['stock_market_link'])
    loader.add_value('stock_market_link', fake_data[1]['stock_market_link'])
    # 构造item
    item = loader.load_item()

    assert_equals(item['stock_market'], 'test1')
    assert_equals(item['stock_market_link'], 'test1')
