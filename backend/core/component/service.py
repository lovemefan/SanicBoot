# -*- coding:utf-8 -*-
# @FileName  :service.py
# @Time      :2023/3/30 00:25
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com


from backend.core import SERVICES_REGISTRY
from backend.core.decorator.singleton import singleton
from backend.model.Service import ServiceBase
from backend.utils.logger import logger
from backend.utils.textProcess import name_convert_to_snake


def Service(cls):
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
    if not issubclass(cls, ServiceBase):
        raise ValueError(
            "Model ({}: {}) must extend ServiceBase".format(name, cls.__name__)
        )

    if name in SERVICES_REGISTRY:
        return SERVICES_REGISTRY[name]

    SERVICES_REGISTRY[name] = singleton(cls)()
    logger.debug(f"Register service {name} success")

    return cls


def get_service(name):
    """get datasource by name"""
    if name not in SERVICES_REGISTRY:
        raise KeyError("Unknown service name: {}".format(name))
    return SERVICES_REGISTRY[name]
