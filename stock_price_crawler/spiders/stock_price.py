# -*- coding: utf-8 -*-
import scrapy
import json
import scrapy.selector
import logging
from scrapy.loader import ItemLoader

from stock_price_crawler.items import StockPriceCrawlerItem


class StockPriceSpider(scrapy.Spider):
    '''
    爬取同花顺行业数据
    '''
    # 爬虫名字
    name = "stock_price"
    # 允许爬取的网站域
    allowed_domains = [r"q.10jqka.com.cn"]
    # 开始爬取的网址
    start_urls = (
        r'http://q.10jqka.com.cn/stock/thshy/',
    )

    def parse(self, response):
        '''
        根据爬取的http://q.10jqka.com.cn/stock/thshy/的信息，得到爬取的网页的页面数，进而构造出填充这个页面的数据的地址
        例如：
        http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/1/quote/quote
        http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/2/quote/quote
        http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/.../quote/quote
        :param response: HtmlResponse，可以提取出Response的body
        :return: Request，爬取填充这个动态网页的数据，得到Response后，调用self.parse_stock_data()
        '''
        # 提取页码
        number_of_total_page_ustr_list = response \
            .css('.page_info') \
            .xpath('./text()') \
            .extract()
        try:
            number_of_total_page = int(number_of_total_page_ustr_list[0]
                                       .split(u'/')[-1])
            if number_of_total_page<1:
                # number_of_total_page的值不合理
                yield None
        except IndexError:
            # 页码提取错误
            yield None

        # 构造填充网页的数据的地址
        page_number = 1
        while page_number <= number_of_total_page:
            # 产生对网页数据的请求
            yield scrapy.Request(
                (
                    'http://q.10jqka.com.cn/'
                    'interface/stock/thshy/'
                    'zdf/desc/{0}/quote/quote'
                ).format(page_number),
                callback=self.parse_stock_data
            )
            page_number = page_number+1

    def parse_stock_data(self, response):
        '''
        爬取填充网页的数据，数据的格式是json
        :param response: HtmlResponse，可以提取出Response的body
        :return: 产生item
        '''
        try:
            data_set = json.loads(response.text)
        except ValueError:
            logging.error('No valid data is returned')
            yield None

        try:
            datum = data_set['data']
        except KeyError:
            logging.error('No data field in JSON')
            yield None

        for element in datum:
            yield self.generate_data_item(element)

    def generate_data_item(self, data):
        loader = ItemLoader(item=StockPriceCrawlerItem())
        try:
            loader.add_value('stock_market', data['platename'])
            # 拼接出行业描述网页的地址
            loader.add_value(
                'stock_market_link',
                '{0}/{1}'.format(
                    'http://q.10jqka.com.cn/stock/thshy',
                    data['hycode']
                )
            )
        except KeyError:
            # data里不包含我们感兴趣的数据
            return None
        return loader.load_item()
