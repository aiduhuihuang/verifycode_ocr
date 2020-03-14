#在主项目目中创建这个文件
#管理控制celery
from celery import Celery
import os
from django.conf import settings
#设置celery的环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Cmdb.settings")
#实例化celery
app=Celery("art_project")#celery服务器名称
#加载celery设置
app.config_from_object("django.conf:settings")
#如果项目中，创建了task.py，那么celery就会沿着app去寻找task.py 文件，来完成任务
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)