# -*- coding: utf-8 -*-
import unittest
import time
from nose.tools import assert_equal
from stock_price_crawler.database import InitDB, DBSession
from stock_price_crawler.models.data import ItemTable


class TestData(unittest.TestCase):
    def setUp(self):
        '''
        连接测试数据库
        :return:
        '''
        self.database = InitDB('test_database.yaml')
        InitDB.Base.metadata.create_all(self.database.engine)
        with DBSession(self.database.Session) as session:
            results = session.query(
                ItemTable
            ).filter(ItemTable.stock_market == 'insert').all()
            map(session.delete, results)

    def tearDown(self):
        '''
        清除测试数据
        :return:
        '''
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
        # 插入之后再取出数据，验证数据项的个数和内容是否一致
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

    def test_insert_with_update(self):
        # 测试insert&update主键，验证数据是否被更新
        value_dict = {
            'stock_market': 'insert&update',
            'stock_market_link': 'test1',
            'scrape_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        obj = ItemTable(database=self.database, **value_dict)
        obj.insert_with_update()
        with DBSession(self.database.Session) as session:
            results = session.query(
                ItemTable
            ).filter(ItemTable.stock_market == 'insert&update').all()
            assert_equal(len(results), 1)
            result = results.pop()
            for key, value in value_dict.iteritems():
                real_value = getattr(result, key)
                if key == 'scrape_time':
                    real_value = real_value.strftime("%Y-%m-%d %H:%M:%S")
                assert_equal(real_value, value)

    def test_update(self):
        value_dict = {
            'stock_market': 'update',
            'stock_market_link': 'test1',
            'scrape_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        obj = ItemTable(database=self.database, **value_dict)
        obj.update()
        with DBSession(self.database.Session) as session:
            results = session.query(
                ItemTable
            ).filter(ItemTable.stock_market == 'update').all()
            assert_equal(len(results), 1)
            result = results.pop()
            for key, value in value_dict.iteritems():
                real_value = getattr(result, key)
                if key == 'scrape_time':
                    real_value = real_value.strftime("%Y-%m-%d %H:%M:%S")
                assert_equal(real_value, value)
