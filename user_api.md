目录
[TOC]
## 1. 接口状态码

| 返回状态（status）  | 描述 |
| --- | --- | 
| AuthenticationFailed | 获取token失败，可能是帐号密码不正确，或者缺少参数 | 
|Unauthorized| 权限不足，无法进行此操作|
|ADD_USER_SUCCESS| 添加用户成功，需要管理员身份|
|UPDATE_USER_SUCCESS| 修改密码成功，需要管理员身份|
|DELETE_USER_SUCCESS|删除用户成功，需要管理员身份|
|QUERY_ALL_USER_SUCCESS| 查询所有的用户成功，需要管理员身份|
|USER_NOT_EXIST|用户不存在|
|MISSPARAMETERS|缺少参数|
##  2. 用户操作说明`(非常重要)`
* 所有的接口发送的参数为json字符串，需要加入以下头部参数如果json格式错误，会返回400 — Bad Request错误
    ```http
    Content-Type: application/json
    ```
* 除了登录接口的所有接口都必须在登录获取token之后，在http的header头部添加如下，才允许访问
    ```http
    Authorization: Bearer <JWT_Token>
    Content-Type: application/json
    ```
    否则返回以下错误
    ```json
    {
      "reasons": [
        "Authorization header not present."
      ],
      "status_code": "Unauthorized"
    }
    ```
    
## 2. 用户登录获得Token

**参数说明**
| 参数    |类型     | 说明|
| --- | --- | ---|
|    username |   str  | 用户名|
|    password |   str  | md5加密后的密码|
**发送参数**
```json
{"username": "lovemefan", "password": "5c5ed1b1b2e95abacda4cc7c8b40d58d"}
```
**测试**
~~~[api]
post:/v1/api/auth

<<<
success
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMzQyMDE0ODY2OTk4ODI5MDU2LCJleHAiOjE2MDkzMjQ4MTR9.Ns5N07ArnvrBv5X0rtf8LMTw3RlCKAO_UgMVh84GYjY"
}
<<<
error
//传参错误
{
  "reasons": [
    "Missing username or password."
  ],
  "status_code": "AuthenticationFailed"
}


//帐号密码不正确
{
  "reasons": [
    "User not found or password is incorrect."
  ],
  "status_code": "AuthenticationFailed"
}
//用户不存在
{
  "reasons": [
    "User not exist."
  ],
  "status_code": "AuthenticationFailed"
}
~~~

##  3.  添加用户

**头部说明**
 ```http
    Authorization: Bearer <JWT_Token>
    Content-Type: application/json
 ```
**参数说明**

| 参数    |类型     | 说明|
| --- | --- | ---|
|    username |   str  |需要创建的用户名|
|    password |   str  | 需要创建的用户md5加密后的密码|
| phone （可选）|str | 手机电话，常用手机号11位，办公电话加上区号十二位 |
| email（可选）           | str  | 邮箱                                             |
| role   | int | 角色ID,0表示普通用户，1表示管理员                |
**发送参数**
```json
{
  "username": "test2",
  "password": 123456,
  "role": 0
}
```
**测试**
~~~[api]
post:/v1/api/user/add_user

<<<
success
{
  "message": "Add user test2 success",
  "status_code": "ADD_USER_SUCCESS",
  "code": 200
}
<<<
error
//缺少用户名
{
  "reasons": [
    "username is empty"
  ],
  "status_code": "MISSPARAMETERS"
}
//缺少密码
{
  "reasons": [
    "password is empty"
  ],
  "status_code": "MISSPARAMETERS"
}
//缺少role_id
{
  "reasons": [
    "user role is empty"
  ],
  "status_code": "MISSPARAMETERS"
}
//role错误  只能为0或1
{
  "reasons": [
    "role id is not 0 or 1"
  ],
  "status_code": "ADD_USER_FAILED"
}
//用户已存在
{
  "reasons": [
    "user test2 is already exist "
  ],
  "status_code": "USER_ALREADY_EXIST"
}
//没有管理员权限，当前用户必须是管理员
{
  "reasons": [
    "You have no authorized to add user information"
  ],
  "status_code": "Unauthorized"
}
//未传入token
{
  "reasons": [
    "Signature has expired."
  ],
  "status_code": "Unauthorized"
}

~~~

##  4.  删除用户
**需要先查询出所有的用户id，传入用户id的参数**
**头部说明**
 ```http
    Authorization: Bearer <JWT_Token>
    Content-Type: application/json
 ```
**参数说明**
| 参数    |类型     | 说明|
| --- | --- | ---|
|  user_id |   str  |需要删除的用户id(必填)|
**发送参数**
```json
{
  "user_id": 1353589026422136832
}
```
**测试**
~~~[api]
post:/v1/api/user/delete_user



<<<
success
{
  "message": "delete test2 Success",
  "status_code": "DELETE_USER_SUCCESS",
  "code": 200
}
<<<
error
//user id 为空
{
  "reasons": [
    "user_id is empty"
  ],
  "status_code": "MISSPARAMETERS"
}
// 没有该用户
{
  "reasons": [
    "User 'test2' is not exist"
  ],
  "status_code": "USER_NOT_EXIST"
}
//未传入token
{
  "reasons": [
    "Signature has expired."
  ],
  "exception": "Unauthorized"
}
//没有管理员权限
{
  "reasons": [
    "You have no authorized to delete user information"
  ],
  "exception": "Unauthorized"
}
~~~

##  5.  修改用户信息包括密码
**需要管理员登录**
**头部说明**
 ```http
    Authorization: Bearer <JWT_Token>
    Content-Type: application/json
 ```
**参数说明**

| 参数    |类型     | 说明|
| --- | --- | ---|
|use_id|int|用户id（必填）|
|    username |   str  |需要修改的用户名|
|    password |   str  | 需要修改后的用户md5加密后的密码|
|  phone |   str  | 手机号（可选）|
|    email |   str  | 邮箱（可选）|
|role|int|角色id，1为管理员，0为普通用户|
|status|int|当前用户状态，0表示不可用，1表示可用|
**发送参数**
```json
{
  "user_id": 1342014866998829056,
  "password": "51fa44eac08481ac17bb844fd8b3335d"
}
```
**测试**
~~~[api]
post:/v1/api/user/modify_user
<<<
success
{
  "message": "Modify test2 Success: ",
  "status_code": "MODIFY_USER_SUCCESS",
  "code": 200
}
<<<
error

//user id 为空
{
  "reasons": [
    "user_id is empty"
  ],
  "status_code": "MISSPARAMETERS"
}

//未传入token
{
  "reasons": [
    "Signature has expired."
  ],
  "status_code": "Unauthorized"
}
//没有管理员权限
{
  "reasons": [
    "You have no authorized to delete user information"
  ],
  "status_code": "Unauthorized"
}
// 用户不存在
{
  "reasons": [
    "User 'User not exist.' is not exist"
  ],
  "status_code": "USER_NOT_EXIST"
}
~~~
## 6. 获取用户自身信息

**头部说明**
 ```http
    Authorization: Bearer <JWT_Token>
    Content-Type: application/json
 ```

**发送参数**
**测试**
~~~[api]
get:/v1/api/auth/me

<<<
success
{
	"me": {
		"user_id": 1342014866998829056,
		"username": "lovemefan",
		"phone": "18679128652",
		"email": "lovemefan@outlook.com",
		"role": 1,
		"create_by": "admin",
		"create_time": "2021-01-24 17:20:27",
		"last_login_time": "2021-01-25 14:22:24",
		"status": 1
	}
}
<<<
error

//没有权限，需要登录
{
  "reasons": [
    "Signature has expired."
  ],
  "status_code": "Unauthorized"
}
~~~
##  7.  管理员查询所有用户


**头部说明**
 ```http
    Authorization: Bearer <JWT_Token>
    Content-Type: application/json
 ```

**测试**
~~~[api]
post:/v1/api/user/get_all_user_information

<<<
success
{
  "message": [
    {
      "uid": 1341983140255768576,
      "username": "admin",
      "phone": null,
      "email": null,
      "password": null,
      "role": 1,
      "create_by": "admin",
      "create_time": "2020-12-30 20:52:38",
      "last_login_time": "2020-12-24 13:37:38",
      "status": 1
    },
    {
      "uid": 1342014866998829056,
      "username": "lovemefan",
      "phone": "18679128652",
      "email": "lovemefan@outlook.com",
      "password": null,
      "role": 1,
      "create_by": "admin",
      "create_time": "2020-12-30 20:52:38",
      "last_login_time": "2020-12-30 21:48:24",
      "status": 1
    }
  ],
  "status_code": "PERMISSION_AVAILABLE",
  "code": 200
}
<<<
error
//未传入token
{
  "reasons": [
    "Signature has expired."
  ],
  "status_code": "Unauthorized"
}
//没有管理员权限
{
  "reasons": [
    "You have no authorized to delete user information"
  ],
  "status_code": "Unauthorized"
}
// 没有任何用户
{
  "reasons": [
    "User 'no user exist' is not exist"
  ],
  "status_code": "USER_NOT_EXIST"
}

~~~
