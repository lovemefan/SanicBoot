# 基于Sanic的后端模板

## 简介

最近使用python做web开发选择web框架的时候，flask并不支持异步，有些异步框架Tornado、Twisted、Gevent 等为了解决性能问题。这些框架在性能上有些提升，但是也有一些问题难以解决。

在python3.6中，官方的异步协程库asyncio正式成为标准。在保留便捷性的同时对性能有了很大的提升,已经出现许多的异步框架使用asyncio。

使用较早的异步框架是aiohttp，它提供了server端和client端，对asyncio做了很好的封装。但是开发方式和最流行的微框架flask不同，flask开发简单，轻量，高效。将两者结合起来就有了sanic。

Sanic框架是和Flask相似异步协程框架，简单轻量，并且性能很高。使用uvloop为核心引擎，使sanic在很多情况下单机并发甚至不亚于Golang。本项目就是以sanic为基础搭建的基本框架。为了提高开发效率，加一些能够复用的部分独立出来以便后续快速开发其他项目。

## 特性

* **使用sanic异步框架，简单，轻量，高效。**
* **使用uvloop为核心引擎，使sanic在很多情况下单机并发甚至不亚于Golang。**
* **项目中使用单例模式实例容器来管理一些类的实列，比如一些服务类的实例，全局只需要创建一次**
* **全局配置文件，不需要重启服务，支持动态更新**
* **使用数据库池连接，提高执行sql语句的效率。**
* **使用sanic-jwt**
* **使用swagger做API标准，能自动生成API文档。**

## 项目功能模块

* **用户管理模块**

## TODO

* 其他公用模块，代码优化，性能优化。
* swagger 相关代码还不完善
* 前端开发。

## 使用到的项目

#### Swagger API

https://github.com/sanic-org/sanic-openapi

![image](https://raw.githubusercontent.com/lovemefan/sanic-backend/master/resources/swagger.png)

#### sanic-jwt

https://github.com/ahopkins/sanic-jwt

## 配置文件

> 设置配置文件采用ini格式配置文件，文件位于backend/config/config.ini 路径下

```ini
[http]
;http端口
port = 80

[log]
;日志等级 有三等， INFO ， DEBUG ， WARNNING
level = INFO
backupCount = 30

[mysql]
db_name = xxx
host = xxx
user = xxx
password = xxx
port=3306
;数据库连接最大复用数，0为无限制
maxusage=1000
```

## 启动服务

首先配置有配置文件中的数据库参数，执行mysql/create_database.sql文件

直接运行 backend/routes/app.py启动，也可以根据Dockerfile启动服务



#### 异常处理

对抛出的异常进行处理，返回统一格式



### 装饰器

#### @Mysql.auto_execute_sql

执行返回的sql语句，返回查询到的元组数组

Example:

```python
@Mysql.auto_execute_sql
def get_user_id(self, username):
    """get user password to validate identify by uesrname
    Args:
        user (User):
    Returns:
       tuple: query result of sql
    """
    sql = f"select uid from user where username = '{username}'"
    return sql
```

##### @Mysql.execute_sql(sql)

执行sql语句，返回到results,可以进一步处理

```python
@Mysql.execute_sql('select * from user')
def get_all_user(self, results):
    users = []
    for row in results:
        user = User(username=row[0])
        users.append(user)
    return users
```


## API

> api文档使用swagger标准。



Example:

```
from sanic import Sanic
from sanic.response import json

from sanic_openapi import doc, swagger_blueprint

app = Sanic()
app.blueprint(swagger_blueprint)


@app.get("/test")
@doc.description('This is a test route with detail description.')
async def test(request):
    return json({"Hello": "World"})
```

#### 相关连接

[swagger](https://sanic-openapi.readthedocs.io/en/stable/index.html)

## Response


## Exception



## 二次开发

### 项目结构

```
.
|-- Dockerfile
|-- config
|   |-- BaseConfig.py
|   |-- Config.py
|   |-- config.ini
|   `-- config.yml
|-- dao
|   |-- DataBasePool.py
|   `-- UserDao.py
|-- decorator
|   |-- mysql.py
|   `-- singleton.py
|-- exception
|   |-- InvalidSystemClock.py
|   `-- UserException.py
|-- model
|   |-- ResponseBody.py
|   `-- User.py
|-- readme.md
|-- requirements.txt
|-- routes
|   |-- app.py
|   |-- banner.txt
|   `-- userRoute
|       `-- UserRoute.py
|-- scripts
|   `-- run-dev.sh
|-- service
|   `-- userService
|       `-- UserService.py
`-- utils
    |-- StatusCode.py
    |-- logger.py
    |-- md5Utils.py
    `-- snowflake.py

```