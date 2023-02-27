#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/21 下午3:28
# @Author  : lovemefan
# @File    : app.py
import os
from time import sleep

from sanic import Sanic, Request, HTTPResponse
import sys
from sanic.exceptions import RequestTimeout, NotFound, Unauthorized, SanicException
from sanic.response import json
from sanic_jwt import initialize, Configuration
from sanic_jwt.exceptions import SanicJWTException
from sanic_openapi import swagger_blueprint

from backend.exception.UserException import UserAddException, UserDeleteException, UserNotExist, MissParameters
from backend.model.ResponseBody import ResponseBody
from backend.routes import blueprint_list
from backend.routes.userRoute.UserRoute import user_route, authenticate, retrieve_user
from backend.service.userService.UserService import UserService
from backend.utils.StatusCode import StatusCode
from backend.utils.logger import logger

sys.path.append(os.path.abspath(os.pardir))

from backend.config.Config import Config

app = Sanic('sanic-backend')
app.blueprint(swagger_blueprint)
app.static("/v1/data", "../../data")


@app.exception(RequestTimeout)
async def timeout(request, exception):
    response = ResponseBody(message=StatusCode.REQUEST_TIMEOUT.name,
                            code=StatusCode.REQUEST_TIMEOUT.value).__dict__
    return json(response, 408)


@app.exception(Unauthorized)
async def timeout(request, exception):
    response = ResponseBody(message=str(exception),
                            code=StatusCode.UNAUTHORIZED.value).__dict__
    return json(response, 403)


@app.exception(NotFound)
async def notfound(request, exception):
    response = ResponseBody(message=f"Requested URL {request.url} not found'",
                            code=StatusCode.NOT_FOUND.value).__dict__
    return json(response, 404)


@app.exception(MissParameters)
async def miss_parameters(request, exception):
    response = ResponseBody(message=str(exception),
                            code=StatusCode.MISS_PARAMETERS.value).__dict__
    return json(response, 401)


@app.exception(UserAddException)
async def add_user_exceptin_handle(request, exception):
    response = ResponseBody(message=str(exception),
                            code=StatusCode.ADD_USER_FAILED.value).__dict__
    return json(response, 401)


@app.exception(UserNotExist)
async def add_user_exceptin_handle(request, exception):
    response = ResponseBody(message=str(exception),
                            code=StatusCode.USER_NOT_EXIST.value).__dict__
    return json(response, 401)


@app.exception(UserDeleteException)
async def delete_user_exceptin_handle(request, exception):
    response = ResponseBody(message=str(exception),
                            code=StatusCode.DELETE_USER_FAILED.value).__dict__
    return json(response, 401)


async def scope_extender(user, *args, **kwargs):
    if user.user_identity is None:
        user_service = UserService()
        user = user_service.get_user_information(user)
    return user.identity


class MyJWTConfig(Configuration):
    user_id = 'username'
    secret = '6K+t6Z+z57uE5qCH5rOo57O757uf'


sainc_init = initialize(app,
                        authenticate=authenticate,
                        configuration_class=MyJWTConfig,
                        retrieve_user=retrieve_user,
                        add_scopes_to_payload=scope_extender,
                        url_prefix='/v1/api/auth')


# replace all response of sanic_jwt with our response body
@sainc_init.app.exception(SanicException)
def sanic_exception_response(request, exception):
    """
    convert sanic response into our response body
    """
    reasons = (
        exception.args[0][0]
        if isinstance(exception.args[0], list)
        else exception.args[0]
    )
    logger.exception(exception)
    return json(ResponseBody(
        message=reasons,
        code=StatusCode.INTERNAL_SERVER_ERROR.value
    ).__dict__, 500)


@sainc_init.app.exception(Exception)
def exception_response(request, exception):
    """
    convert sanic response into our response body
    """
    reasons = (
        exception.args[0][0]
        if isinstance(exception.args[0], list)
        else exception.args[0]
    )
    logger.exception(exception)
    return json(ResponseBody(
        message=reasons,
        code=StatusCode.INTERNAL_SERVER_ERROR.value
    ).__dict__, 500)


@app.middleware("request")
def cors_middle_req(request: Request):
    """路由需要启用OPTIONS方法"""
    if request.method.lower() == 'options':
        allow_headers = [
            'Authorization',
            'content-type'
        ]
        headers = {
            'Access-Control-Allow-Methods':
                ', '.join(request.app.router.get_supported_methods(request.path)),
            'Access-Control-Max-Age': '86400',
            'Access-Control-Allow-Headers': ', '.join(allow_headers),
        }
        return HTTPResponse('', headers=headers)


@app.middleware("response")
def cors_middle_res(request: Request, response: HTTPResponse):
    """跨域处理"""
    allow_origin = '*'
    response.headers.update(
        {
            'Access-Control-Allow-Origin': allow_origin,
        }
    )


# banner文件展示
def load_banner():
    """load the banner"""
    with open('backend/routes/banner.txt', 'r', encoding='utf-8') as f:
        banner = f.read()

    print(banner)


for blueprint_name, blueprint in blueprint_list.items():
    #    logger.info(f"Blueprint: {blueprint_name} registered, Url prefix is:"
    #                f"{blueprint.version_prefix}{blueprint.version}{blueprint.url_prefix}")
    app.blueprint(blueprint)

if __name__ == '__main__':
    # load_banner()
    port = int(Config.get_instance().get('http.port', 80))
    logger.info(f"Server initlized, listenning on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=eval(Config.get_instance().get("server.debug", 'False')))
