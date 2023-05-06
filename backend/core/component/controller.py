# -*- coding:utf-8 -*-
# @FileName  :controller.py
# @Time      :2023/3/30 00:26
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
import inspect
from typing import Union

from sanic import Sanic
from sanic_openapi import swagger_blueprint

from backend.config.Config import Config
from backend.core import CONTROLLERS_REGISTRY
from backend.model.Controller import ControllerBase
from backend.utils.logger import logger
from backend.utils.textProcess import name_convert_to_snake

app = Sanic("sanic-backend")
app.blueprint(swagger_blueprint)


def Controller(cls: Union[str, object]):
    """
    New controller can be added to sanic controller with the :func:`register_controller`
    function decorator.
    For example::
        @Controller
        class UserController(controllerBase):
            (...)
    .. note:: All controller must implement the :class:`controllerBase` interface.
    """

    def _registry_controller(name, uri, cls):
        if name in CONTROLLERS_REGISTRY:
            return CONTROLLERS_REGISTRY[name]

        if isinstance(cls, object):
            if not issubclass(cls, ControllerBase):
                raise ValueError(
                    "Model ({}: {}) must extend controllerBase".format(
                        name, cls.__name__
                    )
                )

        CONTROLLERS_REGISTRY[name] = cls
        logger.debug(f"Register controller {name} to {uri}")
        app.add_route(cls.as_view(), uri)

        return cls

    if inspect.isclass(cls):
        name = name_convert_to_snake(cls.__name__)
        namespace = Config.get_instance().get("server.component.controller")
        uri = f"{cls.__module__}.{cls.__name__}".replace(namespace, "").replace(
            ".", "/"
        )
        uri = "/".join([name_convert_to_snake(i) for i in uri.split("/") if i])
        _registry_controller(name, uri, cls)
    else:

        def decorator(_cls):
            name = name_convert_to_snake(_cls.__name__)
            _registry_controller(name, cls, _cls)

            def wrapper():
                pass

            return wrapper

        return decorator


def get_controller(name):
    """get datasource by name"""
    if name not in CONTROLLERS_REGISTRY:
        raise KeyError("Unknown controller name: {}".format(name))
    return CONTROLLERS_REGISTRY[name]
