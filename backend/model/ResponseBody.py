#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/25 下午9:49
# @Author  : lovemefan
# @File    : ResponseBody.py
class ResponseBody:
    """The response body of http"""

    def __init__(self, message="", data=None, code=None):
        self.message = message
        self.data = data
        self.code = code
