# 基于Sanic的后端模板

[使用文档](https://lovemefan.github.io/sanic-backend/)
## 1. 简介
在python3.6中，官方的异步协程库asyncio正式成为标准。
在保留便捷性的同时对性能有了很大的提升,已经出现许多的异步框架使用asyncio。
Sanic框架是和Flask相似异步协程框架，简单轻量，并且性能很高。
本项目提供一个基于sanic的代码模板，并且封装了一些常用的组件和独有的特性，
可以快速得基于本项目开发一个基于sanic的中小型web服务

## 2. 特性

- 简单轻便
    - 开箱即用，像spring boot一样快速构建属于您的API 应用程序.
      为了提高开发效率，本项目借鉴了spring boot的一些优秀的特性和用法，方便使用python语言快速构建一个web系统，
        可方便用于小型web系统和深度学习模型推理接口的简单搭建。
- 易于拓展
    - 具备sanic优秀的拓展性，随时可以为各种大小的 Web 应用程序提供支持。

## 3. sanic-backend v2.0.0 当前的功能
 1. 配置文件增强

    - [x] yaml配置文件
    - [x] @Value 配置注入到配置类中

 2. 依赖注入

    - [x] @Autowired 注入到service、controller、Dao中
 3. 自动发现与自动注册

    - [x] 自动发现service、controller、model、 dao
    - [x] 自动注册路由

 4. 更多数据库支持,优先级按以下顺序

    - [ ] sqlite
    - [ ] redis
    - [ ] mongodb
    - [ ] PostgreSQL
    - [ ] elasticsearch

 5. 完善文档及注释，增加英文文档

## 4. 使用到的项目

#### Swagger API

https://github.com/sanic-org/sanic-openapi

![image](https://raw.githubusercontent.com/lovemefan/sanic-backend/master/resources/swagger.png)

#### sanic-jwt

https://github.com/ahopkins/sanic-jwt
