# -*- coding:utf-8 -*-
# @FileName  :Datasource.py
# @Time      :2023/3/19 01:22
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
import importlib
import os

from backend.core import DATASOURCE_REGISTRY
from backend.core.datasource.DataBasePoolBase import DataBasePoolBase
from backend.utils.logger import logger


def register_datasource(name):
    """
    New datasource types can be added to sanic datasource with the :func:`register_datasource`
    function decorator.
    For example::
        @register_datasource('mysql')
        class MysqlDatabasePool(DataBasePoolBase):
            (...)
    .. note:: All database must implement the :class:`DataBasePoolBase` interface.
    Args:
        name (str): the name of the datasource
    """

    def register_model_cls(cls):
        if name in DATASOURCE_REGISTRY:
            return DATASOURCE_REGISTRY[name]

        if not issubclass(cls, DataBasePoolBase):
            raise ValueError(
                "Model ({}: {}) must extend DataBasePoolBase".format(name, cls.__name__)
            )

        DATASOURCE_REGISTRY[name] = cls

        return cls

    return register_model_cls


def get_datasource(name):
    """get datasource by name"""
    if name not in DATASOURCE_REGISTRY:
        raise KeyError("Unknown datasource type: {}".format(name))
    return DATASOURCE_REGISTRY[name]


def import_models(models_dir, namespace):
    for file in os.listdir(models_dir):
        path = os.path.join(models_dir, file)
        if (
            not file.startswith("_")
            and not file.startswith("DataBasePoolBase.py")
            and not file.startswith(".")
            and (file.endswith(".py") or os.path.isdir(path))
        ):
            datasource_name = file[: file.find(".py")] if file.endswith(".py") else file
            logger.info("Importing datasource: {}".format(datasource_name))
            importlib.import_module(namespace + "." + datasource_name)


# automatically import any Python files in the models/ directory
models_dir = os.path.dirname(__file__)
import_models(models_dir, "backend.core.datasource")
