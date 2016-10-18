# -*- coding: utf-8 -*-
import unittest

from mock import Mock
from nose.tools import assert_equal

from stock_price_crawler.database import InitDB, DBSession
from stock_price_crawler.models.data import ItemTable


class TestData(unittest.TestCase):
    def setUp(self):
        self.database = InitDB('test_database.yaml')
        InitDB.Base.metadata.create_all(self.database.engine)
        with DBSession(self.database.Session) as session:
            results = session.query(
                ItemTable
            ).filter(ItemTable.stock_market == 'insert').all()
            map(session.delete, results)

    def tearDown(self):
        with DBSession(self.database.Session) as session:
            results = session.query(
                ItemTable
            ).filter(ItemTable.stock_market == 'insert').all()
            map(session.delete, results)

    def test_insert(self):
        value_dict = {
            'stock_market': 'insert',
            'stock_market_link': 'test1',
            'scrape_time': '2016-10-18 00:00:00'
        }
        obj = ItemTable(database=self.database, **value_dict)
        obj.insert()
        # 测试1：插入之后再取出数据，验证数据项的个位和内容是否一致
        with DBSession(self.database.Session) as session:
            results = session.query(
                ItemTable
            ).filter(ItemTable.stock_market == 'insert').all()
            assert_equal(len(results), 1)
            result = results.pop()
            for key, value in value_dict.iteritems():
                real_value = getattr(result, key)
                if key == 'scrape_time':
                    real_value = real_value.strftime("%Y-%m-%d %H:%M:%S")
                assert_equal(real_value, value)
        # 测试2：主键stock_market没变，验证数据是否被更新
        value_dict['stock_market_link'] = 'test2'
        obj = ItemTable(database=self.database, **value_dict)
        obj.insert()
        with DBSession(self.database.Session) as session:
            results = session.query(
                ItemTable
            ).filter(ItemTable.stock_market == 'insert').all()
            assert_equal(len(results), 1)
            result = results.pop()
            for key, value in value_dict.iteritems():
                real_value = getattr(result, key)
                if key == 'scrape_time':
                    real_value = real_value.strftime("%Y-%m-%d %H:%M:%S")
                assert_equal(real_value, value)

                # 测试3：无法mock产生异常的情况?
