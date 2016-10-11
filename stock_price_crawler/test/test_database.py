# -*- coding: utf-8 -*-
import unittest
from mock import mock
from nose.tools import assert_equal
from stock_price_crawler.database import DBConnection, create_engine_with


class TestService(unittest.TestCase):
    def setUp(self):
        '''
        创建engine的mock对象
        :return:
        '''
        self.engine = mock.Mock()

        self.connection = mock.Mock()
        self.connection.close.return_value = None

        self.trans = mock.Mock()
        self.trans.commit.return_value = None
        self.trans.rollback.return_value = None

        self.connection.begin.return_value = self.trans
        self.engine.connect.return_value = self.connection

    def test_DBConnection(self):
        '''
        测试事务提交，回滚方法是否调用，检查连接是否正确关闭
        :return:
        '''
        # 测试1：正常调用DBConnection
        # 检查commit、close的调用状态
        self.trans.commit.assert_not_called()
        self.connection.close.assert_not_called()
        with DBConnection(self.engine) as connection:
            assert_equal(connection, self.engine.connect())
        self.trans.commit.assert_called_with()
        self.connection.close.assert_called_with()

        # 把self.connection.close的状态清空
        self.connection.close.reset_mock()

        # 测试2：不正常调用DBConnection
        # 检查rollback，close的调用状态
        self.trans.rollback.assert_not_called()
        self.connection.close.assert_not_called()
        try:
            with DBConnection(self.engine) as connection:
                connection.execute.side_effect = Exception("Boom!")
                connection.execute()
            assert False
        except:
            assert True
        self.trans.rollback.assert_called_with()
        self.connection.close.assert_called_with()

    def test_create_engine_with(self):
        '''
        测试一个正确配置的test数据库能否正常连接
        :return:
        '''
        # 载入配置文件
        import yaml
        import pkg_resources
        with open(
            pkg_resources.resource_filename(
                'stock_price_crawler.conf',
                'test_database.yml'
            ), 'rb'
        ) as ymlfile:
            config = yaml.load(ymlfile)
        # 测试能否正常连接测试数据库
        try:
            create_engine_with(**config)
            assert True
        except:
            assert False
