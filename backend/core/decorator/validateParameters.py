# -*- coding:utf-8 -*-
# @FileName  :validateParameters.py
# @Time      :2023/2/3 18:56
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com
import numbers
import re
from functools import wraps
from typing import Any, Union

from sanic import json

from backend.model.ResponseBody import ResponseBody
from backend.utils.logger import logger
from backend.utils.StatusCode import StatusCode


async def validata_parameter(data, required, func, *args, **kwargs):
    for parameter in required:
        if data.get(parameter, None) is None:
            response = ResponseBody(
                message=str(f"Missing partial parameter, {parameter} is empty"),
                code=StatusCode.MISS_PARAMETERS.value,
            ).__dict__
            return json(response, 401)

    return await func(*args, **kwargs)


def get_parameters_from_request_by_content_type(request, parameter_type):
    if parameter_type == "all":
        data = {}
        data.update(request.form)
        data.update(dict(request.args))
        data.update(dict(request.files))
        try:
            data.update(dict(request.json))
        except Exception as e:
            logger.error(e)
    elif parameter_type == "json":
        data = dict(request.json)
    elif parameter_type == "form":
        data = dict(request.form)
    elif parameter_type == "args":
        data = dict(request.args)
    elif parameter_type == "files":
        data = dict(request.files)
    else:
        raise ValueError(f"Do not support {parameter_type}")

    return data


def NotEmpty(required: Union[list, tuple], parameter_type: str = "all"):
    """validate
    Args:
        required (list): list of parameters
        parameter_type (str): auto, args, form, json, file
    """

    def decorator(func):
        @wraps(func)
        async def wrap(*args, **kwargs):
            request = args[0]

            if parameter_type == "json" and not request.json:
                logger.debug(
                    "Missing all parameters or Content-Type is not `application/json`."
                )
                response = ResponseBody(
                    message="Please make sure your header has "
                    "`Content-Type: application/json`",
                    code=StatusCode.MISS_PARAMETERS.value,
                )
                return json(response.__dict__)

            data = get_parameters_from_request_by_content_type(request, parameter_type)

            return await validata_parameter(data, required, func, *args, **kwargs)

        return wrap

    return decorator


async def _assert_condition(
    data: dict,
    key,
    condition,
    func,
    message,
    key_type=None,
    string2number=False,
    *args,
    **kwargs,
):
    if data.get(key, None) is None:
        response = ResponseBody(
            message=str(f"Missing partial parameter, {key} is empty"),
            code=StatusCode.INVALID_PARAMETER.value,
        ).__dict__
        return json(response, 401)

    if isinstance(data.get(key), list):
        input_data = data.get(key)[0]
    else:
        input_data = data.get(key)

    if string2number and isinstance(input_data, str):
        try:
            input_data = float(input_data)
        except ValueError:
            logger.error(f"could not convert {key} string to float: '{input_data}'")
            response = ResponseBody(
                message=f"could not convert {key} string to float: '{input_data}'",
                code=StatusCode.INVALID_PARAMETER.value,
            ).__dict__
            return json(response, 401)

    if key_type is not None:
        if not isinstance(input_data, key_type):
            logger.exception(
                f"The data {key} type should be {key_type} type,"
                f"but get  {type(input_data)} type"
            )
            response = ResponseBody(
                message="Server error, please connect developers",
                code=StatusCode.INVALID_PARAMETER.value,
            ).__dict__
            return json(response, 500)

    if condition(input_data):
        return await func(*args, **kwargs)
    else:
        response = ResponseBody(
            message=str(message), code=StatusCode.INVALID_PARAMETER.value
        ).__dict__
        return json(response, 401)


def Length(key, message, min=0, max=0, parameter_type: str = "all"):
    def decorator(func):
        @wraps(func)
        async def wrap(*args, **kwargs):
            request = args[0]
            # todo validate request type
            data = get_parameters_from_request_by_content_type(request, parameter_type)
            return await _assert_condition(
                data,
                key,
                lambda x: True if min <= len(x) <= max else False,
                func,
                message,
                str,
                False,
                *args,
                **kwargs,
            )

        return wrap

    return decorator


def Range(key, message, min=0, max=0, parameter_type: str = "all"):
    def decorator(func):
        @wraps(func)
        async def wrap(*args, **kwargs):
            request = args[0]
            # todo validate request type
            data = get_parameters_from_request_by_content_type(request, parameter_type)
            return await _assert_condition(
                data,
                key,
                lambda x: True if min <= x <= max else False,
                func,
                message,
                numbers.Number,
                True,
                *args,
                **kwargs,
            )

        return wrap

    return decorator


def Assert(
    key,
    condition,
    message,
    parameter_type: str = "all",
    key_type=Any,
    string2number=False,
):
    def decorator(func):
        @wraps(func)
        async def wrap(*args, **kwargs):
            request = args[0]
            # todo validate request type
            data = get_parameters_from_request_by_content_type(request, parameter_type)
            return await _assert_condition(
                data,
                key,
                condition,
                func,
                message,
                key_type,
                string2number,
                *args,
                **kwargs,
            )

        return wrap

    return decorator


def Pattern(
    key: str,
    pattern: str,
    message: str,
    flags=0,
    pattern_mode: str = "match",
    parameter_type: str = "all",
):
    """
    Args:
        key(str): key of requests
        pattern(str): pattern of condition
        message(str): message to return when pattern mismatched
        flags: flags parameter of re module
            re.A # assume ascii "locale"
            re.I # ignore case
            re.L # assume current 8-bit locale
            re.U # assume unicode "locale"
            re.M # make anchors look for newline
            re.S # make dot match newline
            re.X # ignore whitespace and comments
            re.T # disable backtracking
        pattern_mode:  [match or search]. match means equals, search means included.
        parameter_type: [json , args, form, files, args] type of requests
    """

    def decorator(func):
        @wraps(func)
        async def wrap(*args, **kwargs):
            request = args[0]
            # todo validate request type
            data = get_parameters_from_request_by_content_type(request, parameter_type)
            if pattern_mode == "match":
                condition = (
                    lambda x: True if re.match(pattern, x, flags=flags) else False
                )
            elif pattern_mode == "search":
                condition = (
                    lambda x: True if re.search(pattern, x, flags=flags) else False
                )
            else:
                raise ValueError(
                    f"Parameter: pattern_mode {pattern_mode} not supported."
                )

            return await _assert_condition(
                data, key, condition, func, message, str, False, *args, **kwargs
            )

        return wrap

    return decorator


def EnumString(
    key: str, value: Union[list, tuple], message="", parameter_type: str = "all"
):
    def decorator(func):
        @wraps(func)
        async def wrap(*args, **kwargs):
            request = args[0]
            # todo validate request type
            data = get_parameters_from_request_by_content_type(request, parameter_type)
            return await _assert_condition(
                data,
                key,
                lambda x: True if data.get(key, None) in value else False,
                func,
                message,
                str,
                False,
                *args,
                **kwargs,
            )

        return wrap

    return decorator
