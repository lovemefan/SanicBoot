#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 下午11:49
# @Author  : lovemefan
from backend.core.component.autowired import Autowired
from backend.core.component.repository import Repository
from backend.model.Repository import RepositoryBase
from backend.utils.snowflake import IdWorker


@Repository
class UserRepository(RepositoryBase):
    """User operation"""

    def __init__(self):
        pass

    @Autowired
    def mysql(self):
        pass

    @mysql.execute
    def get_all_user():
        sql = """
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
            ON u1.create_by = u2.uid
        """
        return sql

    @mysql.execute
    def get_user_password(username):
        """get user password to validate identify by uesrname
        Args:
            user (User):
        Returns:
           tuple: query result of sql
        """
        sql = f"select password from user where username = '{username}'"
        return sql

    @mysql.execute
    def get_user_id(username):
        """get user password to validate identify by uesrname
        Args:
            user (User):
        Returns:
           tuple: query result of sql
        """
        sql = f"select uid from user where username = '{username}'"
        return sql

    @mysql.execute
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

    @mysql.execute
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

    @mysql.execute
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

    @mysql.execute
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

    @mysql.execute
    def delete_user(self, user):
        if user.username:
            sql = f"delete from user where username='{user.username}'"
        elif user.uid:
            sql = f"delete from user where uid='{user.uid}'"
        return sql

    @mysql.execute
    def login(user):
        """update last_login_time"""
        if user.username:
            sql = f"update user set last_login_time = NOW() where username='{user.username}'"
            return sql
        elif user.uid:
            sql = f"update user set last_login_time = NOW() where username='{user.uid}'"
            return sql
