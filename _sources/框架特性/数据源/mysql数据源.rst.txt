
mysql数据源



.. autoclass:: backend.core.datasource.MysqlDataBasePool.MysqlDataBasePool
    :members:


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
