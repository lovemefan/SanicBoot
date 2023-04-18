#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 下午11:49
# @Author  : lovemefan
from backend.core.component.autowired import Autowired
from backend.core.decorator.datasource import DatasourceDecorator
from backend.model.Dao import DaoBase
from backend.model.User import User
from backend.utils.snowflake import IdWorker

Mysql = DatasourceDecorator("mysql")


class UserDao(DaoBase):
    """User operation"""

    def __init__(self):
        pass

    @Autowired
    def mysql(self):
        pass

    @mysql.execute_sql(
        """
        SELECT u1.uid,
            u1.username,
            u1.phone,
            u1.email,
            u1.user_role,
            u2.username AS create_by,
            u1.create_time,
            u1.last_login_time,
            u1.status
        FROM user AS u1
        LEFT JOIN user AS u2
            ON u1.create_by = u2.uid"""
    )
    def get_all_user(self, results):
        return results

    @mysql.auto_execute_sql
    def get_user_password(self, username):
        """get user password to validate identify by uesrname
        Args:
            user (User):
        Returns:
           tuple: query result of sql
        """
        sql = f"select password from user where username = '{username}'"
        return sql

    @mysql.auto_execute_sql
    def get_user_id(self, username):
        """get user password to validate identify by uesrname
        Args:
            user (User):
        Returns:
           tuple: query result of sql
        """
        sql = f"select uid from user where username = '{username}'"
        return sql

    @mysql.auto_execute_sql
    def get_user_information(self, user):
        """get user password to validate identify by uid when user has login
        Args:
            user (User):
        Returns:
           tuple: query result of sql
        """
        sql = f"""
            SELECT u1.uid,
                u1.username,
                u1.phone,
                u1.email,
                u1.user_role,
                u2.username AS create_by,
                u1.create_time,
                u1.last_login_time,
                u1.status,
                u1.identity
            FROM user AS u1
            LEFT JOIN user AS u2
                ON u1.create_by = u2.uid
            WHERE u1.uid = {user.uid}
        """
        return sql

    @mysql.auto_execute_sql
    def add_user(self, user):
        """
        Args:
            user (User):
        Exception:
            pymysql.err.IntegrityError : The username has exist
        Returns:
           tuple: query result of sql
        """
        uid = IdWorker().get_id()
        sql = f"""
        insert into user(
          uid, username, password, phone, email,
          user_role, create_by
        )
        values
          (
            {uid}, '{user.username}', '{user.password}',
            '{user.phone}', '{user.email}',
            {user.role}, {user.create_by}
          )
        """
        return sql

    @mysql.auto_execute_sql
    def add_user_into_group(self, uid, create_by: int):
        """
        Args:
            user (User):
            create_by (int): the uid of create by
        Exception:
            pymysql.err.IntegrityError : The username has exist
        Returns:
           tuple: query result of sql
        """

        sql = f"insert into group_user(gid,uid) select gid,{uid} from group_user where uid = {create_by}"
        return sql

    @mysql.auto_execute_sql
    def modify_user(self, user):
        """modify user,you can only modify username,password,phone,user_role and status
        Args:
            user (User):
        Returns:
           tuple: query result of sql
        """
        sql = f"""
        update
          user
        set
          username = '{user.username}',
          password = '{user.password}',
          phone = '{user.phone}',
          user_role = {user.role},
          status = {user.status}
        where
          uid = '{user.uid}'
        """
        return sql

    @mysql.auto_execute_sql
    def delete_user(self, user):
        if user.username:
            sql = f"delete from user where username='{user.username}'"
        elif user.uid:
            sql = f"delete from user where uid='{user.uid}'"
        return sql

    @mysql.auto_execute_sql
    def login(self, user):
        """update last_login_time"""
        if user.username:
            sql = f"update user set last_login_time = NOW() where username='{user.username}'"
            return sql
        elif user.uid:
            sql = f"update user set last_login_time = NOW() where username='{user.uid}'"
            return sql


if __name__ == "__main__":
    dao = UserDao()
    user = User(
        username="lovemefan",
        password="5c5ed1b1b2e95abacda4cc7c8b40d58d",
        phone="18679128652",
        email="lovemefan@outlook.com",
        role=1,
        create_by=1341983140255768576,
    )
    res = dao.add_user(user)
    dao.get_all_user()
