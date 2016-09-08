# -*- coding: utf-8 -*-
import scrapy
import json
import scrapy.selector

from stock_price_crawler.items import StockPriceCrawlerItem


class StockPriceSpider(scrapy.Spider):
    name = "stock_price"
    allowed_domains = [r"q.10jqka.com.cn"]
    start_urls = (
        r'http://q.10jqka.com.cn/stock/thshy/',
    )

    def parse(self, response):
        number_of_total_page_ustr_list=response.css('.page_info').xpath('./text()').extract()
        number_of_total_page=int(number_of_total_page_ustr_list[0].split(u'/')[-1])
        page_number=1
        custom_urls=[]
        while page_number<=number_of_total_page:
            custom_urls.append('http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/%d/quote/quote'%page_number)
            page_number=page_number+1
        for stock_data in custom_urls:
            yield scrapy.Request(stock_data,callback=self.parse_stock_data)

    def parse_stock_data(self,response):
        data_set=json.loads(response.text)
        for element in data_set['data']:
            item=StockPriceCrawlerItem()
            item['stock_market'] = element['platename']
            item['stock_market_link'] = '%s/%s' % ('http://q.10jqka.com.cn/stock/thshy', element['hycode'])
            yield item












