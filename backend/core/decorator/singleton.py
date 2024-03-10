#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 下午2:32
# @Author  : lovemefan
# @File    : singleton.py
import multiprocessing
import threading
from functools import wraps

from backend.utils.logger import logger

lock = threading.RLock()
# instance container
instances = {}


def singleton(cls):
    """this is decorator to decorate class , make the class singleton(修饰器实现单例模式)"""

    @wraps(cls)
    def get_instance(*args, **kwargs):
        cls_name = cls.__name__
        process_name = multiprocessing.current_process().name

        # The worker manager and its functionality was introduced in version 22.9.
        # detail see https://sanic.dev/en/guide/running/manager.html#getting-started
        if (
            cls_name not in instances
            and not process_name.startswith("MainProcess")
            and not process_name.startswith("SyncManager")
        ):
            with lock:
                if cls_name not in instances:
                    logger.info(f"creating {cls_name} instance")
                    instance = cls(*args, **kwargs)
                    instances[cls_name] = instance
                    logger.info(f"create {cls_name} instance finished")

            return instances[cls_name]

    return get_instance


def get_all_instance():
    """return all instance in the container"""
    return instances


def function_only_in_sanic_server(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        process_name = multiprocessing.current_process().name
        if not process_name.startswith("MainProcess") and not process_name.startswith(
            "SyncManager"
        ):
            instance = func(*args, **kwargs)
            return instance
        else:
            return None

    return wrapper
