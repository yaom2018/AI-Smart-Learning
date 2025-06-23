# 安装环境
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 数据初始化
## Dev环境
cd drawing-api

```python
python main.py init --env dev # 开发环境
上面的语句执行失败的情况下，执行下面三句
alembic --name dev history
alembic --name dev upgrade head
alembic --name dev current
这三句执行完成后在执行下面的语句
python main.py init --env dev # 开发环境
启动项目
python main.py run

# 访问文档
http://localhost:9000/docs 
```
当使用上面的语句一致更新pro生产数据时请设定 DEBUG = True
"""安全警告: 不要在生产中打开调试运行!"""
# DEBUG = False  # 生产环境请设置为 False
DEBUG = True  # 开发环境请设置为 True 在初始化数据是一定要设置为 True，不然会导致创建表和生成数据不在一个数据库中！！！！！！！！！！！！！！！！！！！！！！

E:\218AiProject\Drawing-Recognition-PC\drawing-api\alembic.ini
## 生产环境
python main.py init

# 接下来启动页面
