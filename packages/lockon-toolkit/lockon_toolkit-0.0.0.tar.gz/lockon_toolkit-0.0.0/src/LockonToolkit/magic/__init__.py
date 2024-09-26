#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/26 上午10:34
# @Author  : @Zhenxi Zhang
# @File    : __init__.py.py
# @Software: PyCharm


import os
import sys
import site
from typing import NoReturn
import os


def mac_env_init_windpy() -> NoReturn:
    """
    初始化 WindPy 环境配置。

    此函数执行以下操作：
    1. 确保用户的站点包目录存在。
    2. 在站点包目录中创建 WindPy.py 的符号链接。
    3. 创建指向 Wind 数据目录的符号链接。

    Raises:
        FileExistsError: 如果目标文件已存在且不是符号链接，则抛出此异常。
        FileNotFoundError: 如果源文件或目录不存在，则抛出此异常。
    """
    # 创建用户站点包目录，如果不存在的话

    _version_py = sys.version.split(" ")[0]

    if _version_py.startswith("3.12"):
        import distutils.sysconfig

        os.system(
            'ln -sf "/Applications/Wind API.app/Contents/python/WindPy.py"'
            + " "
            + distutils.sysconfig.get_python_lib()
        )
        os.system("ln -sf ~/Library/Containers/com.wind.mac.api/Data/.Wind ~/.Wind")

    else:
        user_site_packages = site.getusersitepackages()
        os.makedirs(user_site_packages, exist_ok=True)

        # 创建 WindPy.py 的符号链接
        windpy_src = "/Applications/Wind API.app/Contents/python/WindPy.py"
        windpy_dest = os.path.join(user_site_packages, "WindPy.py")
        os.symlink(windpy_src, windpy_dest)

        # 创建 ~/.Wind 的符号链接指向 ~/Library/Containers/com.wind.mac.api/Data/.Wind
        wind_data_src = "~/Library/Containers/com.wind.mac.api/Data/.Wind"
        wind_data_dest = os.path.expanduser("~/.Wind")
        os.symlink(wind_data_src, wind_data_dest)
