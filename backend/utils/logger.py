#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/21 下午2:05
# @Author  : lovemefan
# @File    : logger.py
import logging
import logging.handlers
import os
# from config import Config
from backend.config.Config import Config

level_map = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(Config.get_instance().get("log.format", None)))
if Config.get_instance().get("log.filename", None) is not None:
    dir = os.path.dirname(Config.get_instance().get("log.filename"))
    if not os.path.exists(dir):
        os.makedirs(dir)
else:
    if not os.path.exists("logs"):
        os.makedirs("logs")
file_stream_handler = logging.handlers.RotatingFileHandler(
    filename=Config.get_instance().get("log.filename", "logs/run.log"),
    maxBytes=int(Config.get_instance().get("log.maxBytes", 102400)),
    backupCount=int(Config.get_instance().get("log.backupCount", 5)),
    )
file_stream_handler.setFormatter(logging.Formatter(Config.get_instance().get("log.format", None)))

logger = logging.getLogger(__name__)

logger.setLevel(level_map[Config.get_instance().get("log.level", "INFO")])
logger.addHandler(stream_handler)
logger.addHandler(file_stream_handler)

logger.info("Logger initialized!")