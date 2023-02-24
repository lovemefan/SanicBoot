#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 下午10:23
# @Author  : lovemefan
# @File    : DBOperation.py
# using lock to make sure get one config at same time
import asyncio
import threading
import time
from typing import Union

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
            autocommit=True,
            **config
        )
        self.__pool_db_init__ = False

    async def execute(self, sql: Union[str, list], query: bool = None, many: bool = False, data: list = None):
        """Execute batch of sql statement method will execute the operation iterating over two ways:

         1. update or insert in same table. insert or replace statements are optimized by batching the data,
            that is using the MySQL multiple rows syntax.
            sql cloud be str or list, if sql type is list, executemany is not available

                Example: Inserting 3 new employees and their phone number

                    data = [
                        ('Jane','555-001'),
                        ('Joe', '555-001'),
                        ('John', '555-003')
                        ]

                    @Mysql.auto_execute_sql
                    def insert_employee(many=True, data)
                        stmt = "INSERT INTO employees (name, phone) VALUES ('%s','%s')"

                    await insert_employee(data)



        2. execute many sql statement in same transaction
            when sql is list, you should specify the query,
            otherwise it will set query type by Determine the first sql statement whether there is a substring of 'select'

                Example: Inserting and update new employees


                    @Mysql.auto_execute_sql
                    def insert_employee(name, query=False)
                        stmt = "INSERT INTO employees (name, phone) VALUES ('%s','%s')"
                        stmt2 = f"UPDATE employees set name={name}"
                        return [stmt, stmt2]

                    await insert_employee(data)
        """
        # execute sql
        if isinstance(sql, str):
            sql = [sql.strip().replace('\n', ' ').replace('  ', ' ')]
            logger.debug(f"Executing {sql}")
        elif isinstance(sql, list):
            sql = [s.strip().replace('\n', ' ').replace('  ', ' ') for s in sql]
            logger.debug(f"Executing many sql in same transaction")

        if query is None:
            if 'select' in sql[0].lower()[:6]:
                query = True
            else:
                query = False

        result = ()
        # if query is None, auto set query is True if select in sql

        if not self.__pool_db_init__:
            self.pool_db = await self.poolDB
            self.__pool_db_init__ = True

        async with self.pool_db.acquire() as conn:
            # set connection into autocommit mode otherwise the 'select' will use wrong cache
            await conn.autocommit(True)
            async with conn.cursor(aiomysql.Cursor) as cursor:
                try:
                    start_time = time.time()
                    if not query:
                        # begin transaction
                        logger.debug(f"Begin transaction ")
                        await conn.begin()

                    # if set many true and update/insert sql and data is list not None, insert all
                    if many and not query and data is not None:
                        if len(sql) != 1:
                            raise ValueError("Using executemany must set sql as str instead of list "
                                             "when set the many true and data not none ")
                        await cursor.executemany(sql[0], data)
                        logger.debug(f"Executing many: {sql[0]} of {data}")
                    else:
                        for s in sql:
                            await cursor.execute(s)
                            logger.debug(f"Executing: {s}")
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


