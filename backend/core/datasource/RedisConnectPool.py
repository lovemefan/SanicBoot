# -*- coding:utf-8 -*-
# @FileName  :RedisConnectPool.py
# @Time      :2023/6/14 21:24
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com

import threading

from backend.core.datasource.RedisConnectionBase import RedisConnectionBase
from backend.utils.logger import logger

lock = threading.RLock()


class RedisClient(RedisConnectionBase):
    __instance = None

    def __init__(self, is_async: bool):
        super().__init__()
        self.host = self.get("redis.host")
        self.port = int(self.get("redis.port"))
        if is_async:
            import redis.asyncio as redis
        else:
            import redis

        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=0)
        self.redis = redis.Redis(connection_pool=self.pool)

    @staticmethod
    def get_instance(*, is_async=True):
        """get a instance at once simultaneously
        Usage:
            redis = RedisClient.get_instance()
            await redis.set('foo', 'bar')

            or

            redis = RedisClient.get_instance(is_async=False)
            redis.set('foo', 'bar')
        """
        if RedisClient.__instance:
            logger.info("Get a redis client success.")
            return RedisClient.__instance
        try:
            lock.acquire()
            if not RedisClient.__instance:
                logger.info("Creating a Redis Pool.")
                RedisClient.__instance = RedisClient(is_async)
                logger.info("Create a Redis Pool finished.")
        finally:
            lock.release()

        logger.info("Init and Get a redis client success.")
        return RedisClient.__instance
