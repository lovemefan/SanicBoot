#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :UserIdentity.py
# @Time      :2023/1/11 14:06
# @Author    :lovemefan
# @email     :lovemefan@outlook.com
from enum import Enum


class UserIdentity(Enum):
    SUPER_ADMIN = 1
    ADMIN = 2
    USER = 3
