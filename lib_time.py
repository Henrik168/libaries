# -*- coding: utf-8 -*-

# global libraries
from datetime import datetime, timedelta
from time import time


def str2timestamp(str_timestamp: str, date_format: str = '%d.%m.%Y %H:%M:%S') -> datetime:
    """
    convert a string into a datetime object
    :param str_timestamp:
    :param date_format:
    :return:
    """
    return datetime.strptime(str_timestamp, date_format)


def str2timedelta(str_time: str, date_format: str = '%H:%M:%S') -> timedelta:
    """
    convert a string into timedelta object
    :param str_time:
    :param date_format:
    :return:
    """
    dt_time = datetime.strptime(str_time, date_format)
    return timedelta(hours=dt_time.hour, minutes=dt_time.minute, seconds=dt_time.second)


def timestamp2strdatetime(timestamp: time, date_format: str = '%d.%m.%Y %H:%M:%S') -> str:
    """
    convert a time object to string.
    :param timestamp: time object (float)
    :param date_format: '%d.%m.%Y %H:%M:%S'
                        '%Y%m%d%H%M%S'
    :return:
    """
    return datetime.fromtimestamp(timestamp).strftime(date_format)


def timestamp2datetime(timestamp: time) -> datetime:
    """
    convert time object to datetime
    :param timestamp:
    :return:
    """
    return datetime.fromtimestamp(timestamp)


def chhop_microseconds(delta: timedelta) -> timedelta:
    """
    chop microseconds from timedelta object.
    :param delta:
    :return:
    """
    return delta - timedelta(microseconds=delta.microseconds)


def time2minute_fraction(delta: timedelta) -> float:
    """
    convert timedelta object to a fraction of minutes
    :param delta:
    :return:
    """
    return delta.total_seconds() / 60
