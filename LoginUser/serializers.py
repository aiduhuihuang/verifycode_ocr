"""
用来对接口返回数据，进行序列化
"""
from rest_framework import serializers
from .models import Goods

class GoodsSerializer(serializers.ModelSerializer):
    #设置出对应字段有choice项
    Goods_Status=serializers.CharField(source='get_Goods_status_display')
    class Meta:
        model=Goods
        fields=["id","Goods_num","Goods_name","Goods_price","Goods_count","Goods_location",
                "Goods_safe_date","Goods_pro_date","Goods_Status",
                "Goods_inprice"]