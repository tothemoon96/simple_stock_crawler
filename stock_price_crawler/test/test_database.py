# -*- coding: utf-8 -*-
from mock import Mock, patch
from nose.tools import assert_equal
from nose.tools import assert_raises
from stock_price_crawler.database import InitDB


@patch('stock_price_crawler.database.create_engine')
@patch('stock_price_crawler.database.sessionmaker')
@patch('stock_price_crawler.database.declarative_base')
def test_InitDB(mock_declarative_base, mock_sessionmaker, mock_create_engine):
    '''
    测试InitDB
    :param mock_declarative_base: declarative_base()
    :param mock_sessionmaker: sessionmaker()
    :param mock_create_engine: create_engine()
    :return:
    '''
    engine = Mock()
    mock_create_engine.return_value = engine
    database_1 = InitDB('test_database.yaml')
    # 测试1：测试的InitDB()正确创建
    # 构造测试数据库的uri
    test_database_uri = 'mysql+mysqlconnector://root:root@localhost:3306/test_stock_price'
    # 检查连接数据库的uri是否正确
    mock_create_engine.assert_called_with(test_database_uri)
    assert_equal(database_1.engine, engine)
    mock_create_engine.assert_called()
    # 检查sessionmaker()调用情况
    mock_sessionmaker.assert_called_with(bind=engine)
    mock_create_engine.assert_called()
    # declarative_base()调用情况，有点问题
    print InitDB.Base
    mock_declarative_base.assert_called()

    # 测试2检查单例模式是否成功构造
    database_2 = InitDB('test_database.yaml')
    assert_equal(database_1, database_2)


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
