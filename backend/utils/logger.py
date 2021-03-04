#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/21 下午2:05
# @Author  : lovemefan
# @File    : logger.py
import logging

from backend.config.Config import Config


def get(key, default=None):
    """get value from config by the key file dynamically
    Args:
        key (str): the key of config file, example `host.ip`.
        default (str): if the key is not exist,return default as value.
    Returns:
        str : the value of config file key example : if the key is `host.ip`
        maybe it will return `localhost`
    """
    return Config.get_instance().get(key, default)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]  - %(levelname)s - %(threadName)s - %(module)s.%(funcName)s - %(message)s')
logger = logging.getLogger(__name__)