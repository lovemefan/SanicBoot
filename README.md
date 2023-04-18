# 基于Sanic的后端模板

## sanic-backend v2.0.0 进一步重构
 1. 配置文件增强

    - [ ] yaml配置文件
    - [ ] @Value 配置注入到配置类中

 2. 依赖注入

    - [ ] @Autowired 注入到service、controller中
 3. 自动发现与自动注册

    - [ ] 自动发现service、controller、model、 dao
    - [ ] 自动注册路由

 4. 更多数据库支持,优先级按一下顺序

    - [ ] sqlite
    - [ ] redis
    - [ ] mongodb
    - [ ] PostgreSQL
    - [ ] elasticsearch

 5. 完善文档及注释，增加英文文档


## 1. 简介

在python3.6中，官方的异步协程库asyncio正式成为标准。在保留便捷性的同时对性能有了很大的提升,已经出现许多的异步框架使用asyncio。

使用较早的异步框架是aiohttp，它提供了server端和client端，对asyncio做了很好的封装。但是开发方式和最流行的微框架flask不同，flask开发简单，轻量，高效。将两者结合起来就有了sanic。

Sanic框架是和Flask相似异步协程框架，简单轻量，并且性能很高。使用uvloop为核心引擎，使sanic在很多情况下单机并发甚至不亚于Golang。本项目就是以sanic为基础搭建的基本框架。为了提高开发效率，加一些能够复用的部分独立出来以便后续快速开发其他项目。

## 2. 特性

* **使用sanic异步框架，简单，轻量，高效。**
* **项目中使用单例模式实例容器来管理service层的实列，全局只需要创建一次**
* **全局配置文件，不需要重启服务，支持动态更新**
* **使用异步数据库aiomysql连接引擎，异步提高执行效率，使用数据库池管理连接，避免浪费大量资源。**
* **使用sanic-jwt作为鉴权模块**
* **使用swagger做API标准，能自动生成API文档。**

## 3. 项目功能模块

* **用户管理模块**

## 4. TODO

* 其他公用模块，代码优化，性能优化。
* swagger 相关代码还不完善
* 前端开发。

## 5. 使用到的项目

#### Swagger API

https://github.com/sanic-org/sanic-openapi

![image](https://raw.githubusercontent.com/lovemefan/sanic-backend/master/resources/swagger.png)

#### sanic-jwt

https://github.com/ahopkins/sanic-jwt

## 6. 配置文件

> 设置配置文件采用ini格式配置文件，文件位于backend/config/config.ini 路径下

```ini
[http]
;http端口
port = 80

[log]
;系统日志等级，日志等级 有三等， INFO ， DEBUG ， WARNNING
level = DEBUG
backupCount = 10
format = [%%(asctime)s] - %%(levelname)s - %%(threadName)s - %%(module)s.%%(funcName)s - %%(message)s
filename = logs/run.log
maxBytes = 102400

[mysql]
db_name = xxx
host = xxx
user = xxx
password = xxx
port=3306
;数据库连接最大复用数，0为无限制
maxusage=1000

[server]
;sanic 是否需要设置debug模式
debug = False
```

## 7. 启动服务

首先配置有配置文件中的数据库参数，执行mysql/create_database.sql文件

直接运行 backend/routes/app.py启动，也可以根据Dockerfile启动服务

或者
```bash
cd sanic-backend

python /SanicExample/backend/app.py
# 或者
gunicorn --bind 0.0.0.0:80 --workers 1  backend.app:app -k uvicorn.workers.UvicornWorker
```



#### 统一异常处理

对抛出的异常进行处理，返回统一格式
#### 配置注入
将配置文件config.yaml中的具体配置注入到python变量当中

```python
from backend.core.component.value import Value

class MysqlConifg:
    @Value('datasource.mysql.host')
    def host(self):
        pass

    @Value('datasource.mysql.port')
    def port(self):
        pass

mysql_config = MysqlConifg
print(mysql_config.host)
print(mysql_config.port)
```

#### 数据校验

```python
@app.route("/test", methods=["POST"])
@NotEmpty(required=['user_name', 'age', 'gender', 'phone'], parameter_type='json')
@Length(key='user_name', min=5, max=20, message='Length of username must in range 18 to 80', parameter_type='json')
@Range(key='age', min=18, max=60, message='Age must in range 18 to 80', parameter_type='json')
@EnumString('gender', value=['male', 'female'], message='gender must male or female', parameter_type='json')
@Pattern('phone', pattern='^1(3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8}$',
         pattern_mode='match', message='phone number invalid', parameter_type='json')
async def test_route(request):
    request.json.get("user_name")
    request.json.get("age")
    request.json.get("gender")
    request.json.get("phone")
    return json({'code': 'ok'})
```
#### 用户鉴权

sanic_jwt自带的@protected()装饰器不能满足多类用户权限控制

使用@authority() 可以用于限制不同用户访问

例如下面接口，可以控制超级管理员和管理员访问
具体实现源码在backend/decorator/authority.py下

```python
@user_route.route('/modify_user', methods=['POST'])
@authority([UserIdentity.SUPER_ADMIN, UserIdentity.ADMIN])
@inject_user()
@NotEmpty(required=['user_id', 'username', 'email', 'password', 'user_role', 'status'], parameter_type='json')
@Pattern('email', pattern='^([a-z0-9A-Z]+[-|\\.]?)+[a-z0-9A-Z]@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-zA-Z]{2,}$',
         pattern_mode='match', parameter_type='json', message='Email format invalid')
async def modify_user(request, user):
    pass
```

#### 数据库操作

* 异常处理及回滚操作
* 执行sql语句自动判断是否需要commit
* 添加批量插入或更新的功能

##### @Mysql.auto_execute_sql


1.根据sgl语句判断是否有select子字符串，查询不执行commit，其他执行commit
```python
@auto_execute_sql
def user_list(self, user_id):
    return f"select *from user where user_id={user_id}"
```
**也可在dao层手动指定是否为查询模式**
```python
@auto_execute_sql
def user_list(self,query=True):
    return 'select * from user'
```

2.增加批量插入或update操作
```python
@auto_execute_sql
def user_list(self, many=True, data):
    return "update user set nick_name='%s', age=%d where name='%s'"

# 调用
# batch of `update/insert` operation execution
data = [('nick_tom', 18, 'tom'), ('nick_jack', 19, 'jack')]
# 此处被auto_execute_sql装饰后变成了一个异步函数，需要await
await user_list(data=data)
```
3. 在同一事务下批量执行多条sql语句
尽量手动指定query，不指定的话，不好判断所有的语句是否需要事务，默认会取出第一条sql语句，如果时select语句
query=True,否则query=False。
```python
@Mysql.auto_execute_sql
def insert_employee(name, query=False)
    stmt = "INSERT INTO employees (name, phone) VALUES ('%s','%s')"
    stmt2 = f"UPDATE employees set name={name}"
    return [stmt, stmt2]

# 调用
await insert_employee(name='tom')

```


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
使用 http://localhost:port/swagger 查看
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

### 相关连接

[swagger](https://sanic-openapi.readthedocs.io/en/stable/index.html)



### 二次开发
* 增加新需求需要 添加route层，service层，dao层。route层只负责参数校验，传递参数；service层负责业务逻辑；
dao层为数据库持久化层。
* 不需要数据库可以删掉DAO层

### 项目结构

```
├── README.md
├── backend
│   ├── Dockerfile
│   ├── app.py
│   ├── config
│   │   ├── BaseConfig.py
│   │   ├── Config.py
│   │   └── config.ini
│   ├── dao
│   │   └── UserDao.py
│   ├── decorator
│   │   ├── authority.py
│   │   ├── mysql.py
│   │   ├── singleton.py
│   │   └── validateParameters.py
│   ├── exception
│   │   ├── InvalidSystemClock.py
│   │   ├── SqlException.py
│   │   └── UserException.py
│   ├── logs
│   │   └── run.log
│   ├── model
│   │   ├── ResponseBody.py
│   │   ├── User.py
│   │   └── UserIdentity.py
│   ├── readme.md
│   ├── requirements.txt
│   ├── routes
│   │   ├── __init__.py
│   │   ├── banner.txt
│   │   └── userRoute
│   │       └── UserRoute.py
│   ├── scripts
│   │   └── run-dev.sh
│   ├── service
│   │   └── userService
│   │       └── UserService.py
│   ├── user_api.md
│   └── utils
│       ├── DataBasePool.py
│       ├── StatusCode.py
│       ├── logger.py
│       ├── md5Utils.py
│       └── snowflake.py
├── docker-compose-dev.yml
├── docker-compose-prod.yml
├── logs
│   └── run.log
├── mysql
│   └── create_database.sql
├── resources
│   └── swagger.png
└── user_api.md
```
