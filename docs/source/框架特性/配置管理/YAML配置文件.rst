YAML配置文件
_________

配置文件
^^^^^^

可自定义添加配置项

.. code-block:: yaml
    :linenos:

    server:
      # name of project
      name: sanic_backend
      http:
        port: 80

      # 尽量不要修改下面的配置，该配置指定了各组件扫描的路径
      # Try not to modify the following configuration,
      # which specifies the path for each component to be scanned
      component:
        controller: "backend.controller"
        service: "backend.service"
        repository: "backend.repository"
        datasource: "backend.core.datasource"

      log:
        debug: false
        backupCount: 10
        format: "[%(asctime)s %(levelname)s ] [%(filename)s:%(lineno)d %(module)s.%(funcName)s] %(message)s"
        filename: "logs/run.log"
        maxBytes: 102400


    datasource:
        mysql:
            db_name: xx
            host: xx
            user: xx
            password: xx
            port: xx
            # 数据库池最大连接数量
            # maximum sizes of the pool.
            max_usage: 1000


获取配置项
^^^^^^^^
获取本地配置有三种方法：

1. 继承BaseConfig类
""""""""""""""""""

.. autoclass:: backend.config.BaseConfig.BaseConfig
    :members:

使用方法
******
.. code-block:: python
    :linenos:

    from backend.config.BaseConfig import BaseConfig

    class Mysql(BaseConfig):
        def __init__():
            self.host = self.get("datasource.mysql.host", 'localhost')
            self.port = self.get("datasource.mysql.port", 80)


2. 使用工具类获取
""""""""""""""
.. autoclass:: backend.config.Config.Config
    :members:

使用方法
******

.. code-block:: python
    :linenos:

    from backend.config.Config import Config
    host = Config.get_instance().get("datasource.mysql.host", "localhost")



3.使用@Value装饰器
""""""""""""""""""

参考 :doc:`@Value的使用 <../依赖注入/配置注入>`。
