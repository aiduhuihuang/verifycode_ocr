from django.urls import path,re_path
from LoginUser.views import *
from rest_framework.routers import SimpleRouter

router=SimpleRouter()
router.register("API/Goods",GoodsViews)
router.register("API/GoodsViewSet",GoodsViewSet)


urlpatterns = [
   #子路由
    path("goods_list/",goods_list),
    re_path("goods_list/(?P<page>\d+)/(?P<status>\d+)/",goods_list),
    re_path("goods_status/(?P<id>\d+)/(?P<status>\w+)/",goods_status),
    #修改商品
    re_path("updategoods/(?P<id>\d+)/",updategoods),


    #个人中心
    path("person/",person),
]
