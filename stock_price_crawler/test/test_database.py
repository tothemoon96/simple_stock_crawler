# -*- coding: utf-8 -*-
import logging
from mock import Mock, patch, PropertyMock
from nose.tools import assert_equal, assert_raises
from sqlalchemy.ext.declarative import DeclarativeMeta

from stock_price_crawler import database
from stock_price_crawler.database import InitDB

logger = logging.getLogger(__name__)


@patch('stock_price_crawler.database.create_engine')
@patch('stock_price_crawler.database.sessionmaker')
@patch('stock_price_crawler.database.Config')
def test_InitDB(mock_Config, mock_sessionmaker, mock_create_engine):
    '''
    测试InitDB
    :param mock_declarative_base: declarative_base()
    :param mock_sessionmaker: sessionmaker()
    :param mock_create_engine: create_engine()
    :return:
    '''
    # 准备测试数据
    engine = Mock()
    mock_create_engine.return_value = engine
    mysql = Mock(
        user='user',
        password='password',
        host='host',
        port='port',
        database='database'
    )
    type(mock_Config.return_value).mysql = PropertyMock(return_value=mysql)
    database_1 = InitDB('test_database.yaml')
    test_database_uri = \
        'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
            'user',
            'password',
            'host',
            'port',
            'database'
        )
    # 测试1：测试的InitDB()正确创建
    # 构造测试数据库的uri
    mock_Config.assert_called_with('test_database.yaml')
    # 检查连接数据库的uri是否正确
    mock_create_engine.assert_called_with(test_database_uri)
    assert_equal(database_1.engine, engine)
    mock_create_engine.assert_called()
    # 检查sessionmaker()调用情况
    mock_sessionmaker.assert_called_with(bind=engine)
    mock_create_engine.assert_called()
    logger.debug(type(InitDB.Base))
    assert isinstance(InitDB.Base, DeclarativeMeta)

    # 测试2：检查单例模式是否成功构造
    database_2 = InitDB('test_database.yaml')
    assert_equal(database_1, database_2)

    # 测试3：检查_database的类型
    assert isinstance(database._database, InitDB)


def test_DBSession():
    # 建立mock对象
    Session = Mock()
    mock_session = Mock()
    mock_session.commit.return_value = None
    mock_session.rollback.return_value = None
    mock_session.close.return_value = None
    Session.return_value = mock_session

    # 测试1：正常调用DBSession
    # 检查commit、close的调用状态
    Session.assert_not_called()
    mock_session.commit.assert_not_called()
    mock_session.close.assert_not_called()
    from stock_price_crawler.database import DBSession
    with DBSession(Session) as session:
        assert_equal(mock_session, session)
    Session.assert_called()
    mock_session.commit.assert_called()
    mock_session.close.assert_called()

    # close的状态清空
    mock_session.close.reset_mock()
    # 测试2：不正常调用DBSession
    # 检查rollback、close的调用状态
    mock_session.rollback.assert_not_called()
    mock_session.close.assert_not_called()

    def _nested_func(Session):
        with DBSession(Session) as session:
            # with语句抛出异常
            raise Exception('Boom!')

    assert_raises(Exception, _nested_func, Session)
    mock_session.rollback.assert_called()
    mock_session.close.assert_called()
