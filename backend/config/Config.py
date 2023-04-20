#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/18 下午3:25
# @Author  : lovemefan
# @File    : config.py
import logging
import os
import threading

import yaml
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# using lock to make sure get one config at same time
lock = threading.RLock()
logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
    level=logging.DEBUG,
)


class ConfigFileModifyHandler(FileSystemEventHandler):
    """Envent handle of config change"""

    def on_modified(self, event):
        logging.debug("updating config ...")
        Config.get_instance().load_config()


class Config:
    """upgrade the config automatically while the config.ini file changed
    Example Config.get_instance().get(key, default)
    """

    # private global attribute of config instance
    __instance = None

    def __init__(self, config_file_path=None):
        """initialize attributions of config class"""
        logging.debug("init config ...")
        self.config_file_path = config_file_path or os.path.join(
            os.path.dirname(__file__), "config.yaml"
        )
        self.load_config()
        self._init_config_file_observer()

    def _init_config_file_observer(self):
        logging.debug("monitor the config file while file changed")
        event_handler = ConfigFileModifyHandler()
        observer = Observer()
        observer.schedule(
            event_handler, path=os.path.dirname(self.config_file_path), recursive=False
        )
        observer.Daemon = True
        observer.start()

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
        logging.debug("loading the config ...")
        with open(file=self.config_file_path, mode="r", encoding="utf-8") as f:
            input = f.read()
            self.config = yaml.safe_load(input)

    def get(self, key, config=None, default=None):
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
                logging.info(f"key is not available,using default value:{default}")
            return config.get(map_key[0], default)
        else:
            option = ".".join(map_key[1:])
            return self.get(option, config.get(map_key[0]), default)
