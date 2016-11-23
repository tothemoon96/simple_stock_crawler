# -*- coding: utf-8 -*-
import datetime
import pytz
from tzlocal import get_localzone

local_tz = get_localzone()


def get_current_time_with_local_time_zone():
    '''
    返回带有当前时区的datetime.datetime对象
    :return:带有当前时区的datetime.datetime对象
    '''
    return local_tz.localize(datetime.datetime.now())


def convert_utc_time_to_local_time(datetime_to_be_converted):
    '''
    将utc时间转换成当地时间，如果参数类型错误，就抛出异常
    :param datetime_to_be_converted:
        要转换的datetime.datetime对象，无论它的timezone是在哪里都认为是utc
    :return: 转换后的timezone对象
    '''
    if (isinstance(datetime_to_be_converted, datetime.datetime)):
        return datetime_to_be_converted.replace(tzinfo=pytz.utc).astimezone(local_tz)
    else:
        raise ValueError(
            'The expected type of the parameter is datetime.datetime'
        )
