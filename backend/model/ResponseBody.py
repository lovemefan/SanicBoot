#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/25 下午9:49
# @Author  : lovemefan
# @File    : ResponseBody.py
from sanic import json


class ResponseBody:
    """The response body of http"""

    def __init__(self, message="", data=None, code=None, status: int = 200):
        self.message = message
        self.data = data
        self.code = code
        self.status = status

    @property
    def response(self):
        return json(
            {"message": self.message, "data": self.data, "code": self},
            status=self.status,
        )
