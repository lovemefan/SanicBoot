项目简介
=============
.. attention::
    最低依赖要求：

    - Python: 3.8+
    - Sanic: 21.9+


- 简单轻便
    - 开箱即用，像spring boot一样快速构建属于您的API 应用程序
- 易于拓展
    - 具备sanic优秀的拓展性，随时可以为各种大小的 Web 应用程序提供支持。

.. note::
    sanic-backend在python3.6中，官方的异步协程库asyncio正式成为标准。
    在保留便捷性的同时对性能有了很大的提升,已经出现许多的异步框架使用asyncio。
    Sanic框架是和Flask相似异步协程框架，简单轻量，并且性能很高。
    使用uvloop为核心引擎，使sanic在很多情况下单机并发甚至不亚于Golang。

.. hint::
    为了提高开发效率，本项目借鉴了spring boot的很多优秀的特性和用法
    ，方便使用python 语言快速构建一个web系统，
    可方便用于小型web系统和深度学习模型推理接口的简单搭建。

sanic-backend 从2021年至今，从本人实验室项目和个人项目重构和迭代过程中，
迭代了两个大的版本

版本变更
_________

- v1.0.0
    - 基于异步数据库aiomysql持久化模块，免去了数据库操作代码以及设置参数和获取结果集的工作
    - 使用sanic-jwt作为鉴权模块
    - 全局ini配置文件
- v2.0.0 正在重构中，借鉴了spring boot部分的设计和使用习惯
    - 全局yaml配置文件
    - 依赖注入
    - 自动发现与注入
    - 更多数据库支持

.. todo::
    1. 配置文件增强

        [√] yaml配置文件

        [√] @Value 配置注入到配置类中

    2. 依赖注入

        [√] @Autowired 注入到service、controller、Dao中

    3. 自动发现与自动注册

        [√] 自动发现service、controller、model、 dao

        [√] 自动注册路由

    4. 更多数据库支持,优先级按以下顺序

        [ ] sqlite

        [ ] redis

        [ ] mongodb

        [ ] PostgreSQL

        [ ] elasticsearch

    5. 完善文档及注释，增加英文文档

.. hint::
    版本v1.0.0已经趋于稳定，并应用于我自己的一些语音识别服务接口中：

    1. `paraformer webserver  <https://github.com/lovemefan/Paraformer-webserver>`_
    #. `whisper webserver <https://github.com/lovemefan/whisper-webserver>`_
    #. `wav2vec2 webserver <https://github.com/lovemefan/Wav2vec2-webserver>`_
