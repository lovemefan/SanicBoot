# -*- coding:utf-8 -*-
# @FileName  :autowired.py
# @Time      :2023/3/30 00:23
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com


from backend.core import CONTROLLERS_REGISTRY, DAO_REGISTRY, SERVICES_REGISTRY
from backend.core.decorator.datasource import DatasourceDecorator
from backend.model.Controller import ControllerBase
from backend.model.Dao import DaoBase
from backend.model.Service import ServiceBase

test_var1 = 2


class Autowired(object):
    """ """

    def __init__(self, fget=None):
        self.fget = fget

    def __get__(self, inst, owner):
        name = self.fget.__name__
        if issubclass(owner, DaoBase):
            globals()[name] = DatasourceDecorator(name)
        elif issubclass(DaoBase):
            return DAO_REGISTRY[name]
        elif issubclass(owner, ServiceBase):
            return SERVICES_REGISTRY[name]
        elif issubclass(owner, ControllerBase):
            return CONTROLLERS_REGISTRY[name]
        else:
            raise KeyError(f"Unknown instance: {inst} which class is {owner}")


class A_class(DaoBase):
    def __init__(self):
        pass

    @Autowired
    def mysql(self):
        pass

    @property
    def abd(self):
        return int


if __name__ == "__main__":
    a = A_class()
    print(a.mysql)
    print(a.test_abd)
