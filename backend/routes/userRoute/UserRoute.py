#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/25 下午3:42
# @Author  : lovemefan
# @File    : UserRoute.py
import pymysql
from sanic import Blueprint
from sanic.response import json
from sanic_jwt import exceptions, inject_user, protected
from sanic_jwt.exceptions import Unauthorized

from backend.core.decorator.validateParameters import Length, NotEmpty, Pattern
from backend.exception.UserException import (
    MissParameters,
    UserAddException,
    UserAlreadyExist,
    UserNotExist,
)
from backend.model.ResponseBody import ResponseBody
from backend.model.User import User
from backend.service.userService.UserService import UserService
from backend.utils.logger import logger
from backend.utils.StatusCode import StatusCode

user_route = Blueprint("user", url_prefix="/api/user", version=1)


@user_route.route("/validate_password", methods=["POST"])
@NotEmpty(required=["username", "password"], parameter_type="json")
@Length(
    "password",
    min=5,
    max=20,
    message="Length of password must be 5 to 20",
    parameter_type="json",
)
async def validate_password(request):
    username = request.json.get("username")
    password = request.json.get("password")

    user = User(username=username, password=password)
    userService = UserService()
    if await userService.validate(user):
        response = ResponseBody(
            message="username or password empty",
            status_code=StatusCode.USERNAME_OR_PASSWORD_EMPTY.name,
        )
    return json(response.__dict__)


async def authenticate(request, *args, **kwargs):
    """validate the user and password and authenticate"""
    print(request.json)
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    userService = UserService()
    user = await userService.get_user_id(User(username=username))

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    try:
        if await userService.validate(User(username=username, password=password)):
            await userService.login(user)
            logger.info(f"User :{user.__dict__}")
            return user
        else:
            raise exceptions.AuthenticationFailed(
                "User not found or password is incorrect."
            )
    except UserNotExist:
        raise exceptions.AuthenticationFailed("User not exist.")


async def retrieve_user(request, payload, *args, **kwargs):
    """return user"""
    print(f"payload:{payload}")
    if payload:
        user_id = payload.get("user_id", None)
        if user_id:
            userService = UserService()
            user = await userService.get_user_information(User(uid=user_id))
            return user
        else:
            return None
    else:
        return None


@user_route.route("/add_user", methods=["POST"])
@inject_user()
@protected()
async def add_user(request, user):
    """add  a user  ,need administrator identify"""
    username = request.json.get("username", None)
    phone = request.json.get("phone", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    role = request.json.get("role", None)
    create_by = user.uid

    if not user.role:
        raise Unauthorized("You have no authorized to add user information")
    if not username:
        raise MissParameters("username is empty")
    elif not password:
        raise MissParameters("password is empty")
    elif role is None:
        raise MissParameters("user role is empty")
    elif role != 0 and role != 1:
        raise UserAddException("role id is not 0 or 1")

    userService = UserService()
    try:
        await userService.add_user(
            User(
                username=username,
                password=password,
                phone=phone,
                email=email,
                role=role,
                create_by=create_by,
            )
        )
    except pymysql.err.IntegrityError:
        raise UserAlreadyExist(username)

    return json(
        ResponseBody(
            message=f"Add user {username} success",
            status_code=StatusCode.ADD_USER_SUCCESS.name,
        ).__dict__,
        200,
    )


@user_route.route("/get_all_user_information", methods=["GET"])
@inject_user()
@protected()
async def get_all_user_information(request, user):
    if not user.role:
        raise Unauthorized("You have no authorized to get user information")

    userService = UserService()
    users = await userService.get_all_user_information()
    response = ResponseBody(
        message=users, status_code=StatusCode.PERMISSION_AVAILABLE.name
    )
    return json(response.__dict__)


@user_route.route("/get_user_information", methods=["GET"])
@inject_user()
@protected()
async def get_user_information(request, user):
    if not request.json:
        raise MissParameters("no parameter send")
    user_id = request.json.get("user_id", None)
    username = request.json.get("username", None)

    if not user.role:
        raise Unauthorized("You have no authorized to get user information")
    if not username:
        raise MissParameters("username is empty")
    if not user.role:
        raise Unauthorized("You have no authorized to get user information")

    userService = UserService()
    if user_id:
        user = await userService.get_user_information(User(uid=user_id))
    else:
        user = await userService.get_user_information(
            await userService.get_user_id(User(username=username))
        )
    response = ResponseBody(
        message=user.to_dict(), status_code=StatusCode.PERMISSION_AVAILABLE.name
    )
    return json(response.__dict__)


@user_route.route("/delete_user", methods=["POST"])
@inject_user()
@protected()
async def delete_user(request, user):
    if not request.json:
        raise MissParameters("no parameter send")
    user_id = request.json.get("user_id", None)
    username = request.json.get("username", None)

    if not user_id:
        raise MissParameters("user_id is empty")
    if not user.role:
        raise Unauthorized("You have no authorized to delete user information")

    userService = UserService()
    delete_user = await userService.get_user_information(
        User(uid=user_id, username=username)
    )
    await userService.delete_user(User(uid=user_id))
    response = ResponseBody(
        message=f"delete {delete_user.username} Success",
        status_code=StatusCode.DELETE_USER_SUCCESS.name,
    )
    return json(response.__dict__)


@user_route.route("/modify_user", methods=["POST"])
@inject_user()
@protected()
@NotEmpty(
    required=["user_id", "username", "email", "password", "user_role", "status"],
    parameter_type="json",
)
@Pattern(
    "email",
    pattern="^([a-z0-9A-Z]+[-|\\.]?)+[a-z0-9A-Z]@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-zA-Z]{2,}$",
    pattern_mode="match",
    parameter_type="json",
    message="Email format invalid",
)
async def modify_user(request, user):
    if not request.json:
        raise MissParameters("no parameter send")
    user_id = request.json.get("user_id", None)
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_role = request.json.get("user_role", None)
    status = request.json.get("status", None)

    if not user_id:
        raise MissParameters("user_id is empty")
    if not user.role:
        raise Unauthorized("You have no authorized to modify user information")

    userService = UserService()
    # Query the user, if the user not exist,raise the UserNotExist exception
    modify_user = await userService.get_user_information(User(uid=user_id))

    # if the parameter of request exist,modify the attribute of user,else do nothing.
    if username:
        modify_user.username = username
    if email:
        modify_user.email = email
    if password:
        modify_user.password = password
    if user_role:
        modify_user.role = user_role
    if status:
        modify_user.status = status

    await userService.modify_user(modify_user)

    response = ResponseBody(
        message=f"Modify {modify_user.username} Success: ",
        status_code=StatusCode.MODIFY_USER_SUCCESS.name,
    )
    return json(response.__dict__)
