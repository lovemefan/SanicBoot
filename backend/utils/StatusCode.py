#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/12 下午10:43
# @Author  : lovemefan
# @File    : statusCode.py
from enum import Enum


class StatusCode(Enum):
    """存储状态的枚举类， 枚举类的值不可相等"""
    """存储状态的枚举类， 枚举类的值不可相等, 增加类别建议全大写下划线分割"""
    SUCCESS = '0000'
    # 请求超时
    REQUEST_TIMEOUT = '0001'
    # 404 not found
    NOT_FOUND = '0002'
    # token 可用
    TOKEN_AVAILABLE = '0003'
    # token 不可用
    TOKEN_NOT_AVAILABLE = '0004'
    # 用户名或密码为空
    USERNAME_OR_PASSWORD_EMPTY = '0005'
    # 用户名或密码错误
    USERNAME_OR_PASSWORD_ERROR = '0006'
    # token 超时失效
    TOKEN_TIMEOUT = '0007'
    # 权限不足
    PERMISSION_DENIED = '0008'
    # 添加用户失败
    ADD_USER_FAILED = '0009'
    # 请求缺少参数
    MISS_PARAMETERS = '0010'
    # 删除用户失败
    DELETE_USER_FAILED = '0011'
    # 修改用户失败
    MODIFY_USER_FAILED = '0012'
    # 用户不存在
    USER_NOT_EXIST = '0013'
    # 未授权
    UNAUTHORIZED = '0014'
    # 参数非法
    INVALID_PARAMETER = '0015'


