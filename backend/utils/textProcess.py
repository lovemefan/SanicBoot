# -*- coding:utf-8 -*-
# @FileName  :convert_name.py
# @Time      :2023/4/20 23:52
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
import re
from typing import Union

from backend.exception.SqlException import SQLException
from backend.utils import logger


def name_convert_to_camel(name: str) -> str:
    """下划线转驼峰(小驼峰)"""
    return re.sub(r"(_[a-z])", lambda x: x.group(1)[1].upper(), name)


def name_convert_to_snake(name: str) -> str:
    """驼峰转下划线"""
    if "_" not in name:
        name = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)
    else:
        raise ValueError(f"{name}字符中包含下划线，无法转换")
    return name.lower()


def name_convert(name: str) -> str:
    """驼峰式命名和下划线式命名互转"""
    is_camel_name = True  # 是否为驼峰式命名
    if "_" in name and re.match(r"[a-zA-Z_]+$", name):
        is_camel_name = False
    elif re.match(r"[a-zA-Z]+$", name) is None:
        raise ValueError(f'Value of "name" is invalid: {name}')
    return name_convert_to_snake(name) if is_camel_name else name_convert_to_camel(name)


fileter_list = [
    "union",
    "#",
    "'",
    "exec",
    "chr ",
    "mid ",
    "*",
    "or ",
    "and ",
    "insert",
    "select",
    "delete",
    "drop",
    "update",
    "count",
    "char(" "master",
    "truncate",
    "declare",
    ";",
    "+",
    "&",
    "/*",
    "*/" "updatexml(",
    "extractvalue(",
    "exp(",
    "load_file(",
    "database(",
]


def filter_invalid_character(*args, **kwargs):
    """
    check the parameters recursion for sql is valid .
    """

    def valid(text: str):
        for _filter in fileter_list:
            if _filter in text.lower():
                logger.error(
                    f"Sql injection warning !!!, filter:{_filter}",
                )
                raise SQLException("Sql injection warning !!!")

    def recursion_valid(data: Union[list, tuple, dict]):
        if isinstance(data, str):
            valid(data)
            return

        if isinstance(data, list) or isinstance(data, tuple):
            for item in data:
                recursion_valid(item)

        if isinstance(data, dict):
            for key, value in data.items():
                recursion_valid(key)
                recursion_valid(value)

    for arg in args + tuple(kwargs.values()):
        recursion_valid(arg)
