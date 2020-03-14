"""DjangoLogin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from LoginUser.views import *

from LoginUser.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    #注册
    path("register/",register),
    #登录
    path("login/",login),
    #用户退出登录
    path("loginout/",loginout),
    #匹配首页
    re_path("^$",index),
    path("index/",index),
    #模板页面
    path("base/",base),

    path("ajax_register/",ajax_register),#用户已存在验证
    path("ajax_pregister/",ajax_pregister),#密码输入不一致验证

    #主路由(商品信息)
    path("loginuser/",include("LoginUser.urls")),
    path("phone/",phone),
    #验证码
    path("verifycode/",verifycode),
    path("test/",test),

    #增加商品
    # path("add/",add_goods),
]

#配置restful

urlpatterns += router.urls
