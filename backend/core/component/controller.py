# -*- coding:utf-8 -*-
# @FileName  :controller.py
# @Time      :2023/3/30 00:26
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
from backend.core import CONTROLLERS_REGISTRY
from backend.model.Controller import ControllerBase


def register_controller(cls):
    """
    New controller can be added to sanic controller with the :func:`register_controller`
    function decorator.
    For example::
        @register_controller()
        class UserController(controllerBase):
            (...)
    .. note:: All controller must implement the :class:`controllerBase` interface.
    """

    name = cls.__name__
    if name in CONTROLLERS_REGISTRY:
        return CONTROLLERS_REGISTRY[name]

    if not issubclass(cls, ControllerBase):
        raise ValueError(
            "Model ({}: {}) must extend controllerBase".format(name, cls.__name__)
        )

    CONTROLLERS_REGISTRY[name] = cls

    return cls


def get_controller(name):
    """get datasource by name"""
    if name not in CONTROLLERS_REGISTRY:
        raise KeyError("Unknown controller name: {}".format(name))
    return CONTROLLERS_REGISTRY[name]
