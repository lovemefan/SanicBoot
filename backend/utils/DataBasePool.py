#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 下午10:23
# @Author  : lovemefan
# @File    : DBOperation.py
# using lock to make sure get one config at same time
import asyncio
import threading
import time
import aiomysql
import pymysql
from backend.config.BaseConfig import BaseConfig
from backend.exception.SqlException import SQLException
from backend.utils.logger import logger

lock = threading.Lock()


class DataBasePool(BaseConfig):
    """DataBase pool
    To get connection from database pool
    Example : DataBasePool.get_instance()
    """
    __instance = None

    def __init__(self):
        config = {
            'host': self.get('mysql.host'),
            'port': int(self.get('mysql.port')),
            'db': self.get('mysql.db_name'),
            'user': self.get('mysql.user'),
            'password': self.get('mysql.password'),
            'charset': 'utf8'
        }
        self.poolDB = aiomysql.create_pool(
            # use pymysql as mysql database driver
            minsize=1,
            loop=asyncio.get_event_loop(),
            # max number usage of one connection,0 or None is no limits,default is 0
            maxsize=int(self.get('mysql.maxusage')),
            **config
        )
        self.__pool_db_init__ = False

    async def execute(self, sql: str, query: bool = None, many: bool = False, data: list = None):
        """execute sql by a connection from database pool
        Args:
            sql (str): sql
            query (bool): is the type of sql is query or else(update insert)
            many (bool): if the many is true, data will be available
            data (list): when many if true, data will be loaded to sql execute
        Returns:
            list: results of sql or None

        Example:

        """
        # execute sql
        sql = sql.strip().replace('\n', ' ').replace('  ', ' ')
        logger.debug(f"Executing {sql}")

        result = ()
        # if query is None, auto set query is True if select in sql

        if not self.__pool_db_init__:
            self.pool_db = await self.poolDB
            self.__pool_db_init__ = True

        async with self.pool_db.acquire() as conn:
            await conn.autocommit(True)
            async with conn.cursor(aiomysql.Cursor) as cursor:
                if query is None:
                    if 'select' in sql.lower()[:6]:
                        query = True
                    else:
                        query = False
                try:
                    start_time = time.time()
                    if not query:
                        # begin transaction
                        logger.debug(f"Begin transaction ")
                        await conn.begin()

                    # if set many true and update/insert sql and data is list not None, insert all
                    if many and not query and data is not None:
                        await cursor.executemany(sql, data)
                    else:
                        await cursor.execute(sql)
                    result = await cursor.fetchall()

                    if not query:
                        await conn.commit()
                        logger.debug(f"Commit finished")

                    end_time = time.time()
                    logger.debug(f"Execute finished in {end_time - start_time:.3} s. "
                                 f"return {result if len(str(result)) < 100 else str(result)[:100] + ' ...'}")
                except pymysql.Error as e:
                    logger.exception(str(e))
                    if not query:
                        await conn.rollback()
                    logger.error(f"Rollback finished")
                    raise SQLException("SQL execution failed.")

        return result

    @staticmethod
    def get_instance():
        """get a instance at once simultaneously"""
        if DataBasePool.__instance:
            return DataBasePool.__instance
        try:
            lock.acquire()
            if not DataBasePool.__instance:
                logger.info('Building DataBase Pool.')
                DataBasePool.__instance = DataBasePool()
                logger.info('Build DataBase Pool finished.')
        finally:
            lock.release()
        return DataBasePool.__instance


