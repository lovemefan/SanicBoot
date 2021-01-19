/*
coding: utf-8
@Time    : 2020/12/23 下午13:30
@Author  : lovemefan

引用阿里java代码规范：
（一）建表规约
    1.【强制】任何字段如果为非负数,必须是 unsigned。
    2.【强制】表名、字段名必须使用小写字母或数字 , 禁止出现数字开头,禁止两个下划线中间只
        出现数字。数据库字段名的修改代价很大,因为无法进行预发布,所以字段名称需要慎重考虑。
        说明:MySQL 在 Windows 下不区分大小写,但在 Linux 下默认是区分大小写。因此,数据库名、表名、
        字段名,都不允许出现任何大写字母,避免节外生枝。
    3.【强制】如果存储的字符串长度几乎相等,使用 char 定长字符串类型。
    4.【参考】合适的字符存储长度,不但节约数据库表空间、节约索引存储,更重要的是提升检索速度。
（二）索引规约
    1.【强制】业务上具有唯一特性的字段,即使是组合字段,也必须建成唯一索引。
        说明:不要以为唯一索引影响了 insert 速度,这个速度损耗可以忽略,但提高查找速度是明显的;
        另外,即使在应用层做了非常完善的校验控制,  只要没有唯一索引,根据墨菲定律,必然有脏数据产生。
    2.【强制】在 varchar 字段上建立索引时,必须指定索引长度,没必要对全字段建立索引,根据
        实际文本区分度决定索引长度。
*/
DROP DATABASE  IF EXISTS `translation_system`;
CREATE DATABASE `translation_system`;
USE `translation_system`;

-- ------------
--   用户相关表
-- ------------


DROP TABLE IF EXISTS `group_user`;
/*小组共享*/
CREATE TABLE `group_user`(
    `gid` bigint unsigned NOT NULL COMMENT '使用雪花算法计算得到的id',
    `uid` bigint unsigned NOT NULL COMMENT '使用雪花算法计算得到的id',
    `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`gid`, `uid`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户组表';

INSERT INTO `group_user`(gid, uid) VALUES (1344262667581399040, 1341983140255768576);
INSERT INTO `group_user`(gid, uid) VALUES (1344262667581399040, 1342014866998829056);

CREATE  INDEX `pk_group_user_gid` ON `group_user` (`gid`);
CREATE UNIQUE INDEX `pk_group_user_uid` ON `group_user` (`uid`);

DROP TABLE IF EXISTS `user`;
/* 创建用户表*/
CREATE TABLE `user`(
    `uid` bigint unsigned NOT NULL COMMENT '使用雪花算法计算得到的id',
    `username` varchar(20) UNIQUE NOT NULL COMMENT '用户昵称|登录帐户',
    `phone` varchar(12) DEFAULT NULL COMMENT '手机电话，常用手机号11位，办公电话加上区号十二位',
    `email` varchar(128) DEFAULT NULL COMMENT '邮箱',
    `password` char(32) NOT NULL COMMENT '密码，固定32个字节的MD5加密字符串',
    `user_role` tinyint unsigned  NOT NULL DEFAULT 0 COMMENT '角色ID,0表示普通用户，1表示管理员',
    `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `create_by` bigint unsigned NOT NULL COMMENT '创建该用户的用户id，只有管理员才能创建用户',
    `last_login_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '最后登录时间',
    `status`  tinyint unsigned DEFAULT '1' COMMENT '1:有效，0:禁止登录',
    PRIMARY KEY (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='用户表';

CREATE UNIQUE INDEX `pk_uid` ON `user` (`uid`);
CREATE UNIQUE INDEX `uk_username` ON `user` (`username`);

INSERT INTO `user` VALUES (1341983140255768576, 'admin', NULL, NULL, 'd6cfa7f078f83d22a4b10169fef95e88', 1, NOW(), 1341983140255768576, '2020-12-24 13:37:38', 1);
INSERT INTO user(uid,username,`password`,phone,email,user_role,create_by) VALUES(1342014866998829056,'lovemefan','5c5ed1b1b2e95abacda4cc7c8b40d58d','18679128652','lovemefan@outlook.com',1,1341983140255768576);
