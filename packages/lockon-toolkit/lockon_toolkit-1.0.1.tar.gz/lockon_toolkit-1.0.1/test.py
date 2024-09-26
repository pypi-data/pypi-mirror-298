#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 下午2:32
# @Author  : @Zhenxi Zhang
# @File    : test.py
# @Software: PyCharm

# %%

from src.LockonToolkit import decorator_utils


@decorator_utils.cached()
def cached_lower(x):
    ...
    return x.lower()


print(cached_lower("CaChInG's FuN AgAiN!"))

# %%
from src.LockonToolkit import dateutils

print(dateutils.get_trade_days_series(start_date="2023-01-01",series_len=12))
