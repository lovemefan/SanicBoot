#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/21 下午3:28
# @Author  : lovemefan
# @File    : app.py
import multiprocessing

from sanic import HTTPResponse, Request
from sanic.exceptions import NotFound, RequestTimeout, SanicException, Unauthorized
from sanic.log import error_logger
from sanic.log import logger as sanic_logger
from sanic.log import server_logger
from sanic.response import json

from backend.config.banner import banner
from backend.config.Config import Config
from backend.controller.user.UserController import Authenticate, RetrieveUser
from backend.core.component.autowired import Autowired
from backend.core.component.controller import app
from backend.exception.UserException import (
    MissParameters,
    UserAddException,
    UserDeleteException,
    UserNotExist,
)
from backend.model.Controller import ControllerBase
from backend.model.ResponseBody import ResponseBody
from backend.utils.logger import logger
from backend.utils.logger import logger as loguru_logger
from backend.utils.StatusCode import StatusCode

process_name = multiprocessing.current_process().name
if process_name.startswith("MainProcess"):
    print(banner)


@app.exception(RequestTimeout)
async def timeout(request, exception):
    response = ResponseBody(
        message=StatusCode.REQUEST_TIMEOUT.name, code=StatusCode.REQUEST_TIMEOUT.value
    ).__dict__
    return json(response, 408)


@app.exception(Unauthorized)
async def unauthorized(request, exception):
    response = ResponseBody(
        message=str(exception), code=StatusCode.UNAUTHORIZED.value
    ).__dict__
    return json(response, 403)


@app.exception(NotFound)
async def notfound(request, exception):
    response = ResponseBody(
        message=f"Requested URL {request.url} not found'",
        code=StatusCode.NOT_FOUND.value,
    ).__dict__
    return json(response, 404)


@app.exception(MissParameters)
async def miss_parameters(request, exception):
    response = ResponseBody(
        message=str(exception), code=StatusCode.MISS_PARAMETERS.value
    ).__dict__
    return json(response, 401)


@app.exception(UserAddException)
async def add_user_exceptin_handle(request, exception):
    response = ResponseBody(
        message=str(exception), code=StatusCode.ADD_USER_FAILED.value
    ).__dict__
    return json(response, 401)


@app.exception(UserNotExist)
async def user_not_exist_handle(request, exception):
    response = ResponseBody(
        message=str(exception), code=StatusCode.USER_NOT_EXIST.value
    ).__dict__
    return json(response, 401)


@app.exception(UserDeleteException)
async def delete_user_exception_handle(request, exception):
    response = ResponseBody(
        message=str(exception), code=StatusCode.DELETE_USER_FAILED.value
    ).__dict__
    return json(response, 401)


class ScopeExtender(ControllerBase):
    @Autowired
    def user_service(self):
        pass

    async def scope_extender(self, user, *args, **kwargs):
        if user.user_identity is None:
            # user_service = UserService()
            user = self.user_service.get_user_information(user)
        return user.identity


@app.middleware("request")
def cors_middle_req(request: Request):
    """路由需要启用OPTIONS方法"""
    if request.method.lower() == "options":
        allow_headers = ["Authorization", "content-type"]
        headers = {
            "Access-Control-Allow-Methods": ", ".join(
                request.app.router.get_supported_methods(request.path)
            ),
            "Access-Control-Max-Age": "86400",
            "Access-Control-Allow-Headers": ", ".join(allow_headers),
        }
        return HTTPResponse("", headers=headers)


@app.middleware("response")
def cors_middle_res(request: Request, response: HTTPResponse):
    """跨域处理"""
    allow_origin = "*"
    response.headers.update(
        {
            "Access-Control-Allow-Origin": allow_origin,
        }
    )


# replace all sanic logger with custom logger
for item in [sanic_logger, error_logger, server_logger]:
    item.info = loguru_logger.info
    item.debug = loguru_logger.debug
    item.warning = loguru_logger.warning
    item.error = loguru_logger.error
    item.exception = loguru_logger.exception

if __name__ == "__main__":
    port = int(Config.get_instance().get("server.http.port", 80))
    logger.info(f"Server initlized, listenning on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
