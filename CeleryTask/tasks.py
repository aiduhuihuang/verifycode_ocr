#编写任务
#导包
from __future__ import absolute_import
from DjangoLogin.celery import app
import time

#无参数的任务
@app.task
def TaskTest():
    #需要执行任务的功能
    time.sleep(30)
    print("helloword")

#有参数的任务
@app.task
def MyPrint(num):
    time.sleep(15)
    print(num)