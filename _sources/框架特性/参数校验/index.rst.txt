参数校验
______


设计参数校验装饰器是为了减少大量重复冗余，且与业务逻辑不太相关的校验代码。

.. important::
    注意⚠️：**参数校验的装饰器得保持@NotEmpty在最上面，其他装饰器可组合, 如下面代码。**

    除@NotEmpty的其他校验装饰器不负责校验值是否存在，所以使用任意校验器都需要配合@NotEmpty使用

.. code-block:: python

    from backend.core.decorator.validateParameters import (
        NotEmpty,
        Length,
        Range,
        EnumString,
        Pattern,
        Assert
    )

    def is_odd(score):
        if score % 2 == 0:
            return False
        else:
            return True

    @Controller
    class TestController(ControllerBase):

        @NotEmpty(required=['user_name', 'age', 'gender', 'phone', 'email', 'number'], parameter_type='json')
        @Length('user_name', min=5, max=20, message='Length of username length must in range 5 to 20', parameter_type='json')
        @Range('age', min=18, max=80, message='Age must in range 18 to 80', parameter_type='json')
        @EnumString('gender', value=['male', 'female'], message='gender must male or female', parameter_type='json')
        @Pattern('phone', pattern='^1(3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8}$',
            pattern_mode='match', message='phone number invalid', parameter_type='json')
        @Pattern('email', pattern='^([a-z0-9A-Z]+[-|\\.]?)+[a-z0-9A-Z]@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-zA-Z]{2,}$',
            pattern_mode='match', parameter_type='json', message='Email format invalid')
        @Assert('number', condition=is_odd, message='The number is not a odd')
        async def post(self, request, user):

            request.json.get("user_name")
            request.json.get("age")
            request.json.get("gender")
            request.json.get("phone")
            request.json.get("email")
            request.json.get("number")
            return json({'code': 'ok'})

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   空值校验
   长度校验
   范围校验
   枚举校验
   正则表达式校验
   断言校验
