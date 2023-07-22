# -*- coding:utf-8 -*-
# @FileName  :RedisConnectionPoolBase.py
# @Time      :2023/6/14 21:21
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
from backend.config.BaseConfig import BaseConfig


class RedisConnectionBase(BaseConfig):
    __instance = None

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        """get a instance at once simultaneously"""
        raise NotImplementedError
