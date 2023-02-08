# -*- coding:utf-8 -*-
# @FileName  :SqlException.py
# @Time      :2023/1/30 20:41
# @Author    :lovemefan
# @email     :lovemefan@outlook.com
from sanic.exceptions import SanicException


class SQLException(SanicException):
    def __init__(self, message):
        super().__init__(message)
