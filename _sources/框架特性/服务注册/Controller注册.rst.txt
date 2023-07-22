Controller注册
_____________

注意事项：

- 自定义的UserController类需要继承ControllerBase父类。
- 需要使用@Controller来装饰自定义的UserController类。
- 类名同样需要使用开头字母大写的驼峰命名法。
- 自定义的UserController类会根据类的路径和实例名来组成当前controller的路由路径。
  例如当前GetAllInfo类路径为backend/controller/user/UserController.py
  该路由者为http://host:port/user/user_controller/get_all_info
- 如果post或get等方法需要使用装饰器，则该装饰器内部需要使用@wraps来继承被装饰方法的属性。
  否则在post方法体里面将不能访问到self.user_service方法

.. code-block:: python
    :linenos:

    # 自动路由
    @Controller
    class GetAllInfo(ControllerBase):
        @Autowired
        def user_service(self):
            pass

        async def post(self, request, user):
            if not user.role:
                raise Unauthorized("You have no authorized to get user information")

            users = await self.user_service.get_all_user_information()
            response = ResponseBody(
                message=users, status_code=StatusCode.PERMISSION_AVAILABLE.name
            )
            return json(response.__dict__)

    # 手动指定路由
    @Controller('/api/getinfo')
    class GetAllInfo(ControllerBase):
        @Autowired
        def user_service(self):
            pass

        async def post(self, request, user):
            if not user.role:
                raise Unauthorized("You have no authorized to get user information")

            users = await self.user_service.get_all_user_information()
            response = ResponseBody(
                message=users, status_code=StatusCode.PERMISSION_AVAILABLE.name
            )
            return json(response.__dict__)
