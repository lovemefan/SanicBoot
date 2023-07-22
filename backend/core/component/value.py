# -*- coding:utf-8 -*-
# @FileName  :value.py
# @Time      :2023/4/18 23:11
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com

from backend.config.Config import Config


class Value(object):
    """
    Used for injecting values into fields from config.yaml

    Args:
        key: the key of config file, such as `server.http.port`
        default: default value, default None

    """

    _config = Config.get_instance()

    def __init__(self, key, default=None):
        self.key = key
        self.default = default

    def __call__(self, inst):
        value = self._config.get(self.key, default=self.default)
        if value is None:
            raise ValueError(f"{self.key} is invalid")
        return value
