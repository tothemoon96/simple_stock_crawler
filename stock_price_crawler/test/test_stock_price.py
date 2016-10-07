# -*- coding: utf-8 -*-
import mock
import pkg_resources
from nose.tools import assert_equal
from scrapy.http import Request, TextResponse
from stock_price_crawler.spiders.stock_price import StockPriceSpider


def fake_response_from_file(file_name, url=None):
    '''
    创建一个Scrapy伪造的HTTP response
    文件从测试目录中读取
    :param file_name: response要用到的仿冒body的文件放置的位置
    :param url:产生request的url
    :return:构造的fake_response
    '''
    # 初始化response的一些要传入的参数url,response
    if url is None:
        url = 'http://www.example.com'
    request = Request(url=url)
    response = None

    # 构造fake_response的body，从而构造出一个fake_response
    with open(
            pkg_resources.resource_filename(
                'stock_price_crawler.test',
                file_name
            ), 'rb'
    ) as file:
        response = TextResponse(
            url=url,
            request=request,
            body=file.read(),
            encoding='utf-8'
        )
    return response


def test_generate_data_item():
    '''
    测试获取的包含行业数据的json的解析是否正确，没测试json里不包含想要的数据的情况
    :return:None
    '''
    # 测试#1
    # 构造仿冒的包含了item所需要的数据的数据源map
    fake_data = {
        "platename": u"非汽车交运",
        "hycode": "fqcjy",
    }
    # 假装启动了爬虫
    spider = StockPriceSpider()
    # 测试爬虫里数据生成的方法
    item = spider.generate_data_item(fake_data)
    # 预设的由fake_data所生成的fake_item，作为预想item正确的值来和item作比较
    fake_item = dict()
    fake_item['stock_market'] = fake_data['platename']
    fake_item['stock_market_link'] = '{0}/{1}' \
        .format('http://q.10jqka.com.cn/stock/thshy', fake_data['hycode'])
    # 校验item
    assert_equal(fake_item, item, u'生成的item不匹配')

    # 测试#2
    # 如果数据生成的方法传入的字典不包含相应的键值对，期望返回一个空值
    # 构造空数据
    fake_data_none = dict()
    item = spider.generate_data_item(fake_data_none)
    # 期待返回一个空值
    assert item is None


@mock.patch.object(StockPriceSpider, 'generate_data_item')
def test_parse_stock_data(mock_generate_data_item):
    '''
    测试根据解析json生成的item项的数目正确与否，没有测试url是否正确
    :param mock_gen: 仿冒的generate_data_item方法，返回值为None
    :return: None
    '''
    # 假装启动了爬虫
    spider = StockPriceSpider()

    # 测试#1
    # 假装返回了一个从json_response_testcase.json中读取内容的response
    fake_response = fake_response_from_file('json_response_testcase.json')
    # 获取parse_stock_data读入response后生成的生成器
    results = spider.parse_stock_data(fake_response)

    # 应该获得50个item
    for index in xrange(50):
        try:
            results.next()
        except StopIteration:
            # 测试数据项的数目是否正确
            assert False

    # 检查mock的generate_data_item是否调用
    assert spider.generate_data_item.called is True

    # 测试#2
    # 假装返回了一个从json_response_testcase_none.json中读取内容的response
    fake_response = fake_response_from_file(
        'json_response_testcase_none.json'
    )
    # 获取parse_stock_data读入response后生成的生成器
    results = spider.parse_stock_data(fake_response)
    # 测试是否能够正确识别空的JSON
    assert results.next() is None


def test_parse():
    '''
    测试获取数据页面的url和数据页面的数目是否正确，没有测试如果解析的html为空的情况
    :return: None
    '''
    # 假装启动了爬虫
    spider = StockPriceSpider()

    # 测试#1
    # 假装返回了一个从page_number_testcase.html中读取内容的response
    fake_response = fake_response_from_file(
        'page_number_testcase.html'
    )
    # 获取parse读入response后生成的生成器
    results = spider.parse(fake_response)
    # 应该获得2个item
    for index in xrange(1, 3):
        try:
            result = results.next()
            assert isinstance(result, Request)
        except StopIteration:
            # 测试返回的url的数目是否正确
            assert False
        # 测试返回的url的地址是否正确
        assert result.url == (
            'http://q.10jqka.com.cn/'
            'interface/stock/thshy/'
            'zdf/desc/{0}/quote/quote'
        ).format(index)

    # 测试#2
    # 测试提取不到页码的情况
    fake_response_none = fake_response_from_file(
        'page_number_testcase_none.html'
    )
    # 获取parse读入response后生成的生成器
    results = spider.parse(fake_response_none)
    # 生成器的结果应该为空
    assert results.next() is None
