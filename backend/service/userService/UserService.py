#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 下午2:18
# @Author  : lovemefan
# @File    : UserService.py
from backend.core.component.autowired import Autowired
from backend.core.component.service import Service
from backend.exception.UserException import UserNotExist
from backend.model.Service import ServiceBase
from backend.model.User import User


@Service
class UserService(ServiceBase):
    """user @singleton to avoid create amount of same instance, improve the efficiency"""

    def __init__(self):
        pass

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
        info = await self.user_repository.get_all_user()
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

    async def get_user_information(self, user: User):
        """query from dbs
        Args:
            user (User): User instance
        Returns:
            User : user information
        """
        info = await self.user_repository.get_user_information(user)

        if len(info) == 0:
            raise UserNotExist(user.username)
        row = info[0]
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
            identity=row[9],
        )

        return user

    async def get_user_id(self, user):
        """get uid by usename"""
        row = await self.user_repository.get_user_id(username=user.username)

        if len(row) == 0:
            raise UserNotExist(user.username)
        uid = row[0]
        user.uid = uid[0]
        return user

    async def add_user(self, user):
        """add User and add user into group
        Args:
            user (User): class instance of User
        Exception:
            pymysql.err.IntegrityError : The username has exist
        """
        await self.user_repository.add_user(user)
        await self.user_repository.add_user_into_group(
            self.get_user_id(user).uid, user.create_by
        )
        return True

    async def modify_user(self, user):
        """modify User you can only modify username,password,phone,user_role and status
        Args:
            user (User): class instance of User
        """
        await self.user_repository.modify_user(user)
        return True

    async def delete_user(self, user):
        """delete User
        Args:
            user (User): class instance of User
        Exception:
            if the user's uid is none, will raise a exception
        """
        await self.user_repository.delete_user(user)
        return True

    async def validate(self, user):
        """validate username and password
        Args:
            user (User): user instance of User class
        Returns:
            bool: if username and password correct return True else return False
        Exception:
            UserNotExist : if the user not exist will raise this exception
        """
        username = user.username
        password = await self.user_repository.get_user_password(username=username)
        if len(password) == 0:
            raise UserNotExist(username)

        password = password[0][0]

        return password == user.password

    async def login(self, user):
        """update last login time"""
        await self.user_repository.login(user)
        return True


if __name__ == "__main__":
    ins1 = UserService()
    ins2 = UserService()

    user = User(
        username="lovemefan",
        uid=1342014866998829056,
        password="5c5ed1b1b2e95abacda4cc7c8b40d58d",
        phone="186******2",
        email="lovemefan@outlook.com",
        role=1,
        create_by=1341983140255768576,
    )
    # res = ins1.get_user_information(User('admin'))
    # print(res)
    # ins2.add_user(user)
    print(ins1.validate(user))
