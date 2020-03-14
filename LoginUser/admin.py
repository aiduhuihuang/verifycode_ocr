from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(LoginUser)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ["pk","email","password","phone_num","gender","age","address","createtime","isDelete"]

#增加供应商表可以增加商品信息
class GoodsInfos(admin.TabularInline):
    model = Goods #关联的外建表
    extra = 4 #附带多少条数据
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ["pk","sup_name","sup_user","sup_sex","sup_email","sup_phone",
                    "sup_status","sup_tel","sup_country","sup_province","sup_area","sup_address"]
    inlines = [GoodsInfos]

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_per_page =15
    list_display = ["pk","Goods_num","Goods_name","Goods_price","Goods_count","Goods_pro_date",
                    "Goods_safe_date","Goods_status","Goods_location","supplier_id"]
