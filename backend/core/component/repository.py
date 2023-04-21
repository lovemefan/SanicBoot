# -*- coding:utf-8 -*-
# @FileName  :dao.py
# @Time      :2023/3/30 01:11
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
from backend.core import REPOSITORY_REGISTRY
from backend.model.Dao import DaoBase
from backend.utils.textProcess import name_convert_to_snake


def Repository(cls):
    """
    New service types can be added to sanic service with the :func:`register_service`
    function decorator.
    For example::
        @register_service()
        class UserService(ServiceBase):
            (...)
    .. note:: All service must implement the :class:`ServiceBase` interface.
    """

    name = name_convert_to_snake(cls.__name__)
    if name in REPOSITORY_REGISTRY:
        return REPOSITORY_REGISTRY[name]

    if not issubclass(cls, DaoBase):
        raise ValueError(
            "Model ({}: {}) must extend DaoBase".format(name, cls.__name__)
        )

    REPOSITORY_REGISTRY[name] = cls

    return cls


def get_dao(name):
    """get datasource by name"""
    if name not in REPOSITORY_REGISTRY:
        raise KeyError("Unknown dao name: {}".format(name))
    return REPOSITORY_REGISTRY[name]
