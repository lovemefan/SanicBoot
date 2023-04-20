# -*- coding:utf-8 -*-
# @FileName  :DatabasePoolBase.py
# @Time      :2023/3/19 01:25
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com

import threading
from typing import Union

from backend.config.BaseConfig import BaseConfig

lock = threading.Lock()


class DataBasePoolBase(BaseConfig):
    """DataBase pool
    To get connection from database pool
    Example : DataBasePool.get_instance()
    """

    __instance = None
    __poolDB = None
    __pool_db_init__ = False

    def __init__(self):
        pass

    async def execute(
        self,
        sql: Union[str, list],
        query: bool = None,
        many: bool = False,
        data: list = None,
    ):
        raise NotImplementedError

    @staticmethod
    def get_instance():
        """get a instance at once simultaneously"""
        raise NotImplementedError
