# -*- coding:utf-8 -*-
# @FileName  :dao.py
# @Time      :2023/3/30 01:11
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
from backend.core import DAO_REGISTRY
from backend.model.Dao import DaoBase


def register_dao(cls):
    """
    New service types can be added to sanic service with the :func:`register_service`
    function decorator.
    For example::
        @register_service()
        class UserService(ServiceBase):
            (...)
    .. note:: All service must implement the :class:`ServiceBase` interface.
    """

    name = cls.__name__
    if name in DAO_REGISTRY:
        return DAO_REGISTRY[name]

    if not issubclass(cls, DaoBase):
        raise ValueError(
            "Model ({}: {}) must extend DaoBase".format(name, cls.__name__)
        )

    DAO_REGISTRY[name] = cls

    return cls


def get_dao(name):
    """get datasource by name"""
    if name not in DAO_REGISTRY:
        raise KeyError("Unknown dao name: {}".format(name))
    return DAO_REGISTRY[name]
