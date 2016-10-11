# -*- coding: utf-8 -*-
from nose.tools import assert_equals
from stock_price_crawler.config import ObjectNotDictError, DictAsClass, Config


def test_ObjectNotDictError():
    '''
    测试stock_price_crawler.config的ObjectNotDictError异常类
    :return:
    '''
    assert_equals(
        'Try to inialize with a non-dict object: test',
        str(ObjectNotDictError('test'))
    )


def test_DictAsClass():
    '''
    测试stock_price_crawler.config的DictAsClass类
    :return:
    '''
    # 测试1：构造正常的字典进行测试
    example = {
        'test': 'test',
        'test_dict': {
            'test': 'test'
        }
    }
    test_ins = DictAsClass(example)
    assert_equals(
        test_ins.test,
        'test'
    )
    assert_equals(
        test_ins.test_dict.test,
        'test'
    )

    # 测试2：测试__getattr__()方法
    assert_equals(test_ins.__getattr__('test'), 'test')

    # 测试3：测试as_dict()方法
    assert_equals(test_ins.as_dict(), example)

    # 测试4：构造会抛出异常的值进行测试
    example = ['test', 'test']
    try:
        test_ins = DictAsClass(example)
        assert False
    except ObjectNotDictError:
        assert True


def test_Config():
    '''
    测试stock_price_crawler.config的Config类
    :return:
    '''
    config = Config('test_config.yml')
    assert_equals(
        config.test.test1,
        'test1'
    )
    assert_equals(
        config.test.test2,
        'test2'
    )
