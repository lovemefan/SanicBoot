#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 下午11:14
# @Author  : lovemefan
# @File    : mysql.py
import inspect
from typing import Union

from backend.utils.DataBasePool import DataBasePool
from backend.utils.logger import logger
from backend.exception.SqlException import SQLException

fileter_list = ['union', '#', "'", 'exec', 'chr ', 'mid ',
                '*', 'or ', 'and ', 'insert', 'select', 'delete', 'drop',
                'update', 'count', 'char('
                'master', 'truncate', 'declare', ';', '+', '&', '/*', '*/'
                'updatexml(', 'extractvalue(', 'exp(', 'load_file(', 'database('
                ]


def filter_invalid_character(*args, **kwargs):
    """
    check the parameters recursion for sql is valid .
    """
    def valid(text: str):
        for filter in fileter_list:
            if filter in text.lower():
                logger.error(f"Sql injection warning !!!, filter:{filter}", )
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



class Mysql:
    @staticmethod
    def execute_sql(sql):
        """this is a decorator to execute sql and autowire result into parameter named results of method
        It uses the DataBase pool to get connection.
        Args:
            sql (str): sql
        Examples:
        @execute_sql(sql='select * from user')
        def user_list(results):
            return results
        Args:
            sql (str): sql
        """

        def decorator(func):
            async def wrap(*args, **kwargs):
                results = await DataBasePool.get_instance().execute(sql)
                return func(*args, **kwargs, results=results)

            return wrap

        return decorator

    @staticmethod
    def auto_execute_sql(func):
        """this is a decorator execute sql from the return of func method and return results of sql execution.
        Examples:
            # when query is True, connection will skip commit operation,
            # if query not set, it will set query by if the `select` string in the sql automatically
            @auto_execute_sql
            def user_list(self, query=True):
                return 'select * from user'

            Call:
                user_list(sql)


            @auto_execute_sql
            def user_list(self, many=True, data):
                return "update user set nick_name='%s', age=%d where name='%s'"

            Call:
                # batch of `update/insert` operation execution
                data = [('nick_tom', 18, 'tom'), ('nick_jack', 19, 'jack')]
                user_list(data=data)

        Returns:
            tuple: results of
        """

        async def wrap(*args, **kwargs):
            filter_invalid_character(*args, **kwargs)
            sql = func(*args, **kwargs)
            query = inspect.signature(func).parameters.get('query', None)
            many = inspect.signature(func).parameters.get('many', False)
            data = kwargs.get('data', None)
            results = await DataBasePool.get_instance().execute(sql, query, many, data)
            return results

        return wrap
