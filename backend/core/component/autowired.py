# -*- coding:utf-8 -*-
# @FileName  :autowired.py
# @Time      :2023/3/30 00:23
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
import inspect

from backend.core import DATASOURCE_REGISTRY, REPOSITORY_REGISTRY, SERVICES_REGISTRY
from backend.model.Controller import ControllerBase
from backend.model.Repository import RepositoryBase
from backend.model.Service import ServiceBase
from backend.utils.textProcess import filter_invalid_character


class Autowired(object):
    """ """

    def __init__(self, fget=None):
        self.fget = fget
        self.name = fget.__name__

    def execute(self, func):
        """this is a decorator execute sql from the return of
        func method and return results of sql execution.

        Examples:
            when query is True, connection will skip commit operation,
            if query not set, it will set query by if the `select` string in the sql automatically

            @auto_execute_sql
            def user_list(self, query=True):
                return 'select * from user'
            @execute
            def user_list(self, many=True, data):
                return "update user set nick_name='%s', age=%d where name='%s'"


            batch of `update/insert` operation execution
            data = [('nick_tom', 18, 'tom'), ('nick_jack', 19, 'jack')]
            user_list(data=data)

        Returns:
            tuple: results of
        """
        if self.name not in DATASOURCE_REGISTRY:
            raise KeyError(f"Unknown datasource: {self.name}")

        async def wrap(*args, **kwargs):
            filter_invalid_character(*args, **kwargs)
            sql = func(*args, **kwargs)
            query = inspect.signature(func).parameters.get("query", None)
            many = inspect.signature(func).parameters.get("many", False)
            data = kwargs.get("data", None)
            results = await DATASOURCE_REGISTRY[self.name]().execute(
                sql, query, many, data
            )
            return results

        return wrap

    def __get__(self, inst, owner):
        """call for autowired attribute

        Args:
            inst: instance decoratored  by Autowired
            owner: owner class of instance

        Returns:

        """
        name = self.fget.__name__
        try:
            if issubclass(owner, RepositoryBase):
                self.instance = DATASOURCE_REGISTRY[name]
                return DATASOURCE_REGISTRY[name]
            elif issubclass(owner, ServiceBase):
                self.instance = REPOSITORY_REGISTRY[name]
                return REPOSITORY_REGISTRY[name]
            elif issubclass(owner, ControllerBase):
                self.instance = SERVICES_REGISTRY[name]
                return SERVICES_REGISTRY[name]
        except KeyError:
            raise KeyError(f"Unknown name: {name} in {inst}")
