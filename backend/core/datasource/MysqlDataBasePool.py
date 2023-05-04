#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 下午10:23
# @Author  : lovemefan
# @File    : DBOperation.py
# using lock to make sure get one config at same time
import threading
import time
from abc import ABC
from typing import Union

import aiomysql
import pymysql

from backend.core.datasource import Datasource
from backend.core.datasource.DataBasePoolBase import DataBasePoolBase
from backend.core.decorator.singleton import singleton
from backend.exception.SqlException import SQLException
from backend.utils.logger import logger

lock = threading.RLock()


@singleton
@Datasource("mysql")
class MysqlDataBasePool(DataBasePoolBase, ABC):
    """DataBase pool To get connection from database pool"""

    def __init__(self):
        super().__init__()
        config = {
            "host": self.get("datasource.mysql.host"),
            "port": int(self.get("datasource.mysql.port")),
            "db": self.get("datasource.mysql.db_name"),
            "user": self.get("datasource.mysql.user"),
            "password": self.get("datasource.mysql.password"),
            "charset": "utf8",
        }
        self.__poolDB = aiomysql.create_pool(
            # use pymysql as mysql database driver
            minsize=1,
            # loop=asyncio.get_event_loop(),
            # max number usage of one connection,
            # 0 or None is no limits,default is 0
            maxsize=int(self.get("datasource.mysql.max_usage")),
            autocommit=True,
            **config,
        )
        self.__pool_db_init__ = False

    async def execute(
        self,
        sql: Union[str, list],
        query: bool = None,
        many: bool = False,
        data: list = None,
        return_affected: bool = False,
    ):
        """Execute batch of sql statement method will execute the operation iterating over two ways:

        Args:
            sql(str): the sql statement
            query(bool): if query is true, it would not call with transaction
            many(bool): if many is true, support insert or replace statements are optimized by batching
            data(bool): if many is true, support insert or replace statements by batching data
            return_affected(bool): if set return_affected,
                will return all the sqls' number of rows that has been produced of affected
                the document intro will be
                found @https://aiomysql.readthedocs.io/en/latest/cursors.html


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
            otherwise it will set query type by Determine
            the first sql statement whether there is a substring of 'select'

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
            sql = [sql.strip().replace("\n", " ").replace("  ", " ")]
            logger.debug(f"Executing {sql}")
        elif isinstance(sql, list):
            sql = [s.strip().replace("\n", " ").replace("  ", " ") for s in sql]
            logger.debug("Executing many sql in same transaction")

        if query is None:
            if "select" in sql[0].lower()[:6]:
                query = True
            else:
                query = False

        result = ()
        # if query is None, auto set query is True if select in sql

        if not self.__pool_db_init__:
            self.__poolDB = await self.__poolDB
            self.__pool_db_init__ = True

        async with self.__poolDB.acquire() as conn:
            # set connection into autocommit mode otherwise the 'select' will use wrong cache
            await conn.autocommit(True)
            async with conn.cursor(aiomysql.Cursor) as cursor:
                try:
                    start_time = time.time()
                    if not query:
                        # begin transaction
                        logger.debug("Begin transaction ")
                        await conn.begin()

                    # if set many true and update/insert sql and data is list not None, insert all
                    if many and not query and data is not None:
                        if len(sql) != 1:
                            raise ValueError(
                                "Using executemany must set sql as str instead of list "
                                "when set the many true and data not none "
                            )
                        await cursor.executemany(sql[0], data)
                        logger.debug(f"Executing many: {sql[0]} of {data}")
                    else:
                        affected_rows = []
                        for s in sql:
                            affected_rows.append(await cursor.execute(s))
                            logger.debug(f"Executing: {s}")
                    result = await cursor.fetchall()

                    if not query:
                        await conn.commit()
                        logger.debug("Commit finished")

                    end_time = time.time()
                    logger.debug(
                        f"Execute finished in {end_time - start_time:.3} s. "
                        f"return {result if len(str(result)) < 100 else str(result)[:100] + ' ...'}"
                    )
                except pymysql.Error as e:
                    logger.exception(str(e))
                    if not query:
                        await conn.rollback()
                    logger.error("Rollback finished")
                    raise SQLException("SQL execution failed.")

        if return_affected:
            # if set return_affected,
            # will return all the sqls' number of rows that has been produced of affected
            # the document intro will be
            # found @https://aiomysql.readthedocs.io/en/latest/cursors.html
            return (result, affected_rows)
        else:
            return result
