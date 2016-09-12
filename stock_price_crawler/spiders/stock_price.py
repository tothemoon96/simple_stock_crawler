# -*- coding: utf-8 -*-
import scrapy
import json
import scrapy.selector
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
        number_of_total_page_ustr_list = response\
            .css('.page_info')\
            .xpath('./text()')\
            .extract()
        number_of_total_page = int(number_of_total_page_ustr_list[0]
                                   .split(u'/')[-1])
        # 构造填充网页的数据的地址
        page_number = 1
        custom_urls = []
        while page_number <= number_of_total_page:
            custom_urls.append('http://q.10jqka.com.cn/'
                               'interface/stock/thshy/'
                               'zdf/desc/%d/quote/quote'
                               % page_number)
            page_number = page_number+1
        for stock_data in custom_urls:
            # 产生对网页数据的请求
            yield scrapy.Request(stock_data,
                                 callback=self.parse_stock_data)

    def parse_stock_data(self, response):
        '''
        爬取填充网页的数据，数据的格式是json
        :param response: HtmlResponse，可以提取出Response的body
        :return: 产生item
        '''
        data_set = json.loads(response.text)
        for element in data_set['data']:
            item = StockPriceCrawlerItem()
            item['stock_market'] = element['platename']
            # 根据json的信息，拼接出行业描述网页的地址
            item['stock_market_link'] = '%s/%s' \
                                        % ('http://q.10jqka.com.cn/'
                                           'stock/thshy',
                                           element['hycode'])
            # 生成item
            yield item
