# -*- coding:utf-8 -*-
# @FileName  :Controller.py
# @Time      :2023/3/30 00:56
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
from sanic.views import HTTPMethodView


class ControllerBase(HTTPMethodView):
    def __init__(self):
        super(ControllerBase, self).__init__()
