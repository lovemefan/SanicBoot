#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :authority.py
# @Time      :2023/1/11 14:00
# @Author    :lovemefan
# @email     :lovemefan@outlook.com
from copy import deepcopy
from functools import wraps
from inspect import isawaitable

from sanic.views import HTTPMethodView
from sanic_jwt import utils
from sanic_jwt.decorators import _do_protection, instant_config
from sanic_jwt.exceptions import Unauthorized

from backend.model.UserIdentity import UserIdentity


def authority(user_identity=None, require_all=False, require_all_actions=True, **kw):
    if user_identity is None:
        user_identity = [UserIdentity.USER]

    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if issubclass(request.__class__, HTTPMethodView):
                request = args[0]

            if user_identity is not None and user_identity is not False:
                protect_kwargs = deepcopy(kwargs)
                protect_kwargs.update(
                    {
                        "initialized_on": None,
                        "kw": kw,
                        "request": request,
                        "f": f,
                        "return_response": False,
                    }
                )
                _, instance = await _do_protection(*args, **protect_kwargs)

                if request.method == "OPTIONS":
                    return instance

                with instant_config(instance, request=request, **kw):
                    current_user_identity = await instance.ctx.auth.extract_scopes(
                        request
                    )
                    override = instance.ctx.auth.override_scope_validator
                    destructure = instance.ctx.auth.destructure_scopes
                    if current_user_identity is None:
                        # If there are no defined scopes in the payload,
                        # deny access
                        is_authorized = False
                        reasons = "Invalid user identity."
                        raise Unauthorized(reasons)

                    else:
                        is_authorized = await validate_identity(
                            request,
                            user_identity,
                            current_user_identity,
                            require_all=require_all,
                            require_all_actions=require_all_actions,
                            override=override,
                            destructure=destructure,
                            request_args=args,
                            request_kwargs=kwargs,
                        )
                        if not is_authorized:
                            reasons = "Invalid user_identity."
                            raise Unauthorized(reasons)

            # the user is authorized.
            # run the handler method and return the response
            # NOTE: it's possible to use return await.utils(f, ...) in
            # here, but inside the @protected decorator it wont work,
            # so this is left as is for now
            response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response
            return response

        return decorated_function

    return decorator


async def validate_identity(
    request,
    user_identity,
    current_user_identity,
    override,
    destructure,
    require_all=True,
    require_all_actions=True,
    request_args=[],
    request_kwargs={},
):
    scopes = await utils.call(destructure, user_identity)
    scopes = await utils.call(scopes, request, *request_args, **request_kwargs)

    if not isinstance(scopes, (list, tuple)):
        scopes = [scopes]

    method = all if require_all else any
    return method(
        validate_single_identity(
            x,
            current_user_identity,
            require_all_actions=require_all_actions,
            override=override,
        )
        for x in scopes
    )


def validate_single_identity(
    required, user_scopes, require_all_actions=True, override=None
):
    if not user_scopes:
        return False

    elif user_scopes.count(None) > 0:
        if user_scopes.count(None) == len(user_scopes):
            return False

        user_scopes = list(filter(lambda v: v is not None, user_scopes))

    user_scopes = [x for x in user_scopes]

    is_valid = False

    for requested in user_scopes:
        valid_namespace = required.value == requested

        is_valid = all([valid_namespace])

        if is_valid:
            break

    outcome = (
        override(is_valid, required, user_scopes, require_all_actions)
        if callable(override)
        else is_valid
    )
    return outcome
