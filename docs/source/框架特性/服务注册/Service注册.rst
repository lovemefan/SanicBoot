Service注册
____________

注意事项：

- 自定义的UserService类需要继承ServiceBase父类。
- 需要使用@Service来装饰自定义的UserService类，目的是将自定义的UserService注册到系统当中，方便Controller层注入。
- 类名同样需要使用开头字母大写的驼峰命名法。
- 自定义的UserRepository类会注册为转换成小写以下划线分割的实例名，使用
- 被@mysql.execute装饰后，原方法会变成一个异步方法，因此在Service及上层需要使用await调用。
  如下面第18行代码所示。

.. code-block:: python
    :linenos:

    from backend.core.component.autowired import Autowired
    from backend.core.component.service import Service
    from backend.model.Service import ServiceBase

    @Service
    class UserService(ServiceBase):
        @Autowired
        def user_repository(self):
            pass

        async def get_all_user_information(self):
            """query from dbs
            Args:
                user (User): User instance
            Returns:
                User : user information
            """
            info = await self.user_dao.get_all_user()
            users = []
            for row in info:
                user = User(
                    uid=row[0],
                    username=row[1],
                    phone=row[2],
                    email=row[3],
                    role=row[4],
                    create_by=row[5],
                    create_time=row[6],
                    last_login_time=row[7],
                    status=row[8],
                )
                users.append(user.__dict__)

            return users
