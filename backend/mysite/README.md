# 使用说明

首先，查看setting.py，查看数据库连接密码等是否正确，并手动在数据库引擎中创建数据库，但不用建表。

之后，依次输入以下命令，可以自动在数据库中建表

`python manage.py makemigrations`

`python manage.py migrate`

之后，输入以下命令，让程序运行：

`python manage.py runserver`

编写api代码的话，有两个地方：mysite/api.py和mysite.py/urls.py