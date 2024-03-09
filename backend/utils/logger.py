# -*- coding:utf-8 -*-
# @FileName  :logger.py
# @Time      :2023/8/8 20:17
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com

import sys

from loguru import logger

from backend.config.Config import Config

retention = Config().get_instance().get("server.log.retention", "10 days")
save_path = Config().get_instance().get("server.log.sava_path", "./logs/{time}.log")
log_level = Config().get_instance().get("server.log.level", "DEBUG")
_format = Config().get_instance().get("server.log.format", None)
logger.remove()
logger.add(save_path, retention=retention, format=_format, level=log_level)
logger.add(sys.stdout, colorize=True, format=_format, level=log_level)
