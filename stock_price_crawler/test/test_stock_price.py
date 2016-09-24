# -*- coding: utf-8 -*-
import collections
import mock
from nose.tools import assert_equals
from scrapy.http import Request,TextResponse
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
        response=TextResponse(url=url,request=request,body=file.read(),encoding='utf-8')
    return response

def convert(data):
    '''
    将dict中的str转换成unicode，每个item根据其value的类型递归向下进行转换
    :param data:dict
    :return:一个key和value都为unicode的字典
    '''
    if isinstance(data, basestring):
        return unicode(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def test_generate_data_item():
    '''
    测试获取的包含行业数据的json的解析是否正确，没测试json里不包含想要的数据的情况
    :return:无
    '''
    #构造仿冒的包含了item所需要的数据的数据源map
    fake_data={
        "platename": u"非汽车交运",
        "platecode": "881127",
        "num": "16",
        "jj": "12.35",
        "zxj": "3383.24",
        "cjl": "161.13",
        "cje": "19.90",
        "zdf": "0.65",
        "zde": "21.74",
        "type": "1",
        "hycode": "fqcjy",
        "py": "F",
        "gainername": u"*ST钱江",
        "gainercode": "000913",
        "ledname": u"众合科技",
        "ledcode": "000925",
        "gainerzdf": "4.99",
        "gainerzxj": "17.87",
        "ledzdf": "-2.53",
        "ledzxj": "21.97",
        "jlr": "-0.02",
        "rtime": "2016-09-24 10:35:51"
    }
    #假装启动了爬虫
    spider=StockPriceSpider()
    #测试爬虫里数据生成的方法
    item=spider.generate_data_item(fake_data)
    #校验item的键值
    for key,value in fake_data.iteritems():
        if key in ['platename','hycode']:
            if 'platename' in key:
                key='stock_market'
            elif 'hycode' in key:
                key='stock_market_link'
                value='{0}/{1}'.format('http://q.10jqka.com.cn/stock/thshy',value)
            assert_equals(value,item[key])

@mock.patch.object(StockPriceSpider,'generate_data_item')
def test_parse_stock_data(mock_gen):
    '''
    测试根据解析json生成的item项的数目正确与否，没有测试url是否正确
    :param mock_gen: 仿冒的generate_data_item方法，返回值为None
    :return: 无
    '''
    # 假装启动了爬虫
    spider=StockPriceSpider()

    # 假装返回了一个从json_response_testcase.json中读取内容的response
    fake_response = fake_response_from_file('.\\stock_price_crawler\\test\\json_response_testcase.json')
    # 获取parse_stock_data读入response后生成的生成器
    results = spider.parse_stock_data(fake_response)
    #应该获得50个item
    for index in xrange(50):
        try:
            results.next()
        except StopIteration:
            assert False

    #假装返回了一个从json_response_testcase_none.json中读取内容的response
    fake_response = fake_response_from_file('.\\stock_price_crawler\\test\\json_response_testcase_none.json')

    # 获取parse_stock_data读入response后生成的生成器
    results = spider.parse_stock_data(fake_response)
    assert results.next() is None