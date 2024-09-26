#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 上午11:32
# @Author  : @Zhenxi Zhang
# @File    : __init__.py.py
# @Software: PyCharm
import datetime
import json
import pkgutil
import typing

import pandas as pd

bytes_flow = pkgutil.get_data(__name__, "./trade_days_calendar/a_stock_calendar.json")
a_stock_calendar = pd.Series(json.loads(bytes_flow))
a_stock_calendar.index = pd.to_datetime(a_stock_calendar.index)
_a_stock_trading_days = set(a_stock_calendar.keys())


def date2dtdate(date_input: typing.Union[str, pd.Timestamp, datetime.date]):
    """
    将输入日期转换为 Pandas Timestamp 的日期部分。

    参数:
        date_input (Union[str, pd.Timestamp]): 输入日期，可以是字符串或 Pandas Timestamp。

    返回:
        pd.Timestamp: 转换后的日期部分。

    示例:
        >>> date2dtdate('2023-01-01')
        Timestamp('2023-01-01 00:00:00')

        >>> date2dtdate(pd.Timestamp('2023-01-01'))
        Timestamp('2023-01-01 00:00:00')
    """
    dt64 = pd.to_datetime(date_input)
    return dt64.date()


def date2str_(date_input: typing.Union[str, pd.Timestamp]) -> str:
    """
    将日期输入转换成字符串YYYY-MM—DD表示形式。

    参数
    ----
    date_input : str 或 pandas.Timestamp
        需要转换的日期输入。
        这可以是一个表示日期的字符串，
        或者是一个 pandas Timestamp 对象。

    返回
    ----
    str
        日期的字符串表示形式。

    示例
    ----
    >>> date2str_('2024-09-25')
    '2024-09-25'

    >>> date2str_(pd.Timestamp('2024-09-25'))
    '2024-09-25'
    """
    dt64 = pd.to_datetime(date_input)
    return str(dt64.date())


def date2str(date_input: typing.Union[str, pd.Timestamp]) -> str:
    """
        将日期输入转换成无分隔符的字符串表示形式。

        参数
        ----
        date_input : str 或 pandas.Timestamp
            需要转换的日期输入。
            这可以是一个表示日期的字符串，
            或者是一个 pandas Timestamp 对象。

        返回
        ----
        str
            去掉日期分隔符（如短横线）的日期字符串。

        示例
        ----
        >>> date2str('2024-09-25')
        '20240925'
    _—
        >>> date2str(pd.Timestamp('2024-09-25'))
        '20240925'
    """
    dt64 = pd.to_datetime(date_input)
    return str(dt64.date()).replace("-", "")


def get_next_trade_date(
    date: typing.Union[str, pd.Timestamp, datetime.date]
) -> datetime.date:
    """
    获取输入日期的下一个交易日。

    参数
    ----
    date : str 或 pandas.Timestamp
        输入的日期，可以是字符串或 pandas Timestamp 类型。

    返回
    ----
    datetime.date
        输入日期之后的下一个交易日的日期。

    示例
    ----
    >>> get_next_trade_date('2024-09-25')
    datetime.date(2024, 9, 26)
    """
    date_dt64 = pd.to_datetime(date)
    while date_dt64 not in _a_stock_trading_days:
        date_dt64 += datetime.timedelta(days=1)
    # 如果输入日期已经是交易日，返回下一个交易日
    current_index = a_stock_calendar[str(date_dt64.date())]
    if current_index < len(a_stock_calendar) - 1:
        next_date_str = list(a_stock_calendar.keys())[current_index + 1]
        return date2dtdate(next_date_str)
    else:
        # 如果已经是最后一个交易日，返回当前日期
        return date2dtdate(str(date_dt64.date()))


def get_last_trade_date(
    date: typing.Union[str, pd.Timestamp, datetime.date]
) -> datetime.date:
    """
    获取输入日期的上一个交易日。

    参数
    ----
    date : str 或 pandas.Timestamp 或 datetime.date
        输入的日期，可以是字符串、pandas Timestamp 或 datetime.date 类型。

    返回
    ----
    datetime.date
        输入日期之前的上一个交易日的日期。
    """
    date_dt64 = pd.to_datetime(date)
    while date_dt64 not in _a_stock_trading_days:
        date_dt64 -= datetime.timedelta(days=1)
    # 如果输入日期已经是交易日，返回下一个交易日
    current_index = a_stock_calendar[str(date_dt64.date())]
    if current_index < len(a_stock_calendar) - 1:
        next_date_str = list(a_stock_calendar.keys())[current_index - 1]
        return date2dtdate(next_date_str)
    else:
        # 如果已经是最后一个交易日，返回当前日期
        return date2dtdate(str(date_dt64.date()))


def get_trade_days_series(
    start_date: typing.Union[str, pd.Timestamp], series_len: int
) -> typing.List[datetime.date]:
    """
    获取一系列连续的交易日。

    参数
    ----
    start_date : str 或 pandas.Timestamp
        开始日期，可以是字符串或 pandas Timestamp 类型。

    series_len : int
        交易日序列的长度。

    返回
    ----
    List[datetime.date]
        包含一系列连续交易日的列表。
    """
    current_date = date2dtdate(start_date)
    trade_days = []
    for _ in range(series_len):
        current_date = get_next_trade_date(current_date)
        trade_days.append(current_date)
    return trade_days


def is_trade_date(date: typing.Union[str, pd.Timestamp, datetime.date]) -> bool:
    """
    判断给定日期是否为交易日。

    参数
    ----
    date : str 或 pandas.Timestamp 或 datetime.date
        需要判断的日期，可以是字符串、pandas Timestamp 或 datetime.date 类型。

    返回
    ----
    bool
        如果给定日期是交易日则返回 True，否则返回 False。
    """
    date_dt64 = pd.to_datetime(date)
    return date_dt64 in a_stock_calendar.index
