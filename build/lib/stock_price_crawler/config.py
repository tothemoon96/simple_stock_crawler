# -*- coding: utf-8 -*-
#
# Author: QianfuFinance
#
'''
    从yaml文件中获取配置
'''
import yaml
import pkg_resources


class ObjectNotDictError(Exception):
    '''
        异常类，当 ``ClassAsDict`` 的初始化参数非字典类型时抛出
    '''
    def __init__(self, dic):
        self.dic = dic

    def __str__(self):
        return 'Try to inialize with a non-dict object: {0}'.format(
            self.dic
        )


class DictAsClass(object):
    '''
        特殊字典类，实现了按属性取字典键值
    '''
    def __init__(self, dic):
        # 要求传入类型为字典
        if not isinstance(dic, dict):
            raise ObjectNotDictError(dic)

        self.__dict__ = dic

        # 递归转换字典为特殊字典类
        for key, value in self.__dict__.iteritems():
            if isinstance(value, dict):
                # 这个方法递归的把yml读入的字典的键值对转换为该类的属性
                self.__dict__[key] = DictAsClass(value)

    def __getattr__(self, key):
        return self.__dict__.get(key)

    def as_dict(self):
        return self.__dict__


class Config(DictAsClass):
    '''
        配置文件类
    '''
    def __init__(self, filename):
        with open(
            pkg_resources.resource_filename(
                'stock_price_crawler.conf',
                '{0}'.format(filename)
            ), 'rb'
        ) as ymlfile:
            super(Config, self).__init__(yaml.load(ymlfile))
