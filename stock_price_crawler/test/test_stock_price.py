# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.http import TextResponse
import mock
from stock_price_crawler.spiders.stock_price import StockPriceSpider

def fake_response_from_file(file_name,url=None):
    '''
    创建一个Scrapy伪造的HTTP response
    文件从测试目录中读取
    :param file_name: response要用到的仿冒body的文件放置的位置
    :param url:产生request的url
    :return:构造的fake_response
    '''
    #初始化response的一些要传入的参数url,response
    if url is None:
        url = 'http://www.example.com'
    request = Request(url=url)
    response=None

    #构造fake_response的body，从而构造出一个fake_response
    with open(file_name,'rb') as file:
        response=TextResponse(url=url,request=request,body=file.read())
        response.encoding='utf-8'
    return response

@mock.patch.object(StockPriceSpider,'parse_stock_data')
def test_parse_json_response(mock_list):
    '''
    测试获取的包含行业数据的json的解析是否正确
    :param mock_list:被装饰器包装过的参数
    :return:无
    '''
    #假装启动了爬虫
    spider=StockPriceSpider()
    #从json中读取到了数据，构造了一个fake_response
    fake_response=fake_response_from_file('json_response_testcase.json',url='http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/1/quote/quote')
    #获取parse_stock_data爬取了数据之后的生成器





