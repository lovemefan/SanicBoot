#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :authority.py
# @Time      :2023/1/11 14:00
# @Author    :lovemefan
# @email     :lovemefan@outlook.com

from functools import wraps

import jwt

from backend.model.ResponseBody import ResponseBody
from backend.utils.StatusCode import StatusCode


def check_token(request):
    if not request.token:
        return False

    try:
        jwt.decode(request.token, request.app.config.SECRET, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return ResponseBody(
                    "You are unauthorized.", code=StatusCode.UNAUTHORIZED, status=401
                )

        return decorated_function

    return decorator(wrapped)
