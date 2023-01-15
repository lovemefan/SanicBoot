#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :__init__.py
# @Time      :2023/1/15 13:48
# @Author    :lovemefan
# @email     :lovemefan@outlook.com
from backend.routes.userRoute.UserRoute import user_route

blueprint_list = {
    'user_route': user_route,
}