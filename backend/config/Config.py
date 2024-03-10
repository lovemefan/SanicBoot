#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/18 下午3:25
# @Author  : lovemefan
# @File    : config.py

import os
import sys
import threading

import yaml
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> |<yellow>[{process.name}:{process}]</yellow> "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
    "- <level>{message}</level>",
)
# using lock to make sure get one config at same time
lock = threading.RLock()


class Config:
    """upgrade the config automatically while the config.ini file changed
    Example Config.get_instance().get(key, default)
    """

    # private global attribute of config instance
    __instance = None

    def __init__(self, config_file_path=None):
        """initialize attributions of config class"""
        self.config_file_path = config_file_path or os.path.join(
            os.path.dirname(__file__), "config.yaml"
        )
        self.load_config()

    @staticmethod
    def get_instance():
        """get a instance at once simultaneously"""

        if not Config.__instance:
            with lock:
                if not Config.__instance:
                    Config.__instance = Config()

        return Config.__instance

    def load_config(self):
        """load the config file"""
        with open(file=self.config_file_path, mode="r", encoding="utf-8") as f:
            input = f.read()
            self.config = yaml.safe_load(input)

    def get(
        self,
        key,
        default=None,
        config=None,
    ):
        """get value by the key from config

        Args:
            key (str): format [section].[key] example: app.name
            config (dict): config
            default: if the key not exist ,return default value
        Returns:
            str: value of key, if the key not exist ,return default value
        """
        map_key = key.split(".")
        config = config or self.config
        if not isinstance(config, dict):
            return config
        if len(map_key) == 1:
            if map_key[0] not in config.keys():
                logger.info(
                    f"{map_key[0]} is not available,using default value:{default}"
                )
            return config.get(map_key[0], default)
        else:
            option = ".".join(map_key[1:])
            return self.get(option, default=default, config=config.get(map_key[0]))
