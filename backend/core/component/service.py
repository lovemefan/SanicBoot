# -*- coding:utf-8 -*-
# @FileName  :service.py
# @Time      :2023/3/30 00:25
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
from backend.core import SERVICES_REGISTRY
from backend.model.Service import ServiceBase


def register_service(cls):
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
    if name in SERVICES_REGISTRY:
        return SERVICES_REGISTRY[name]

    if not issubclass(cls, ServiceBase):
        raise ValueError(
            "Model ({}: {}) must extend ServiceBase".format(name, cls.__name__)
        )

    SERVICES_REGISTRY[name] = cls

    return cls


def get_service(name):
    """get datasource by name"""
    if name not in SERVICES_REGISTRY:
        raise KeyError("Unknown service name: {}".format(name))
    return SERVICES_REGISTRY[name]
