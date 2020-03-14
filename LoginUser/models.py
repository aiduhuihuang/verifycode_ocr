from django.db import models

# Create your models here.
ISDELETE_STATUS=((0,"否"),(1,"是"))
GENDER_STATUS=((0,"女"),(1,"男"))
GOODS_STATUS=((0,"在售"),(1,"停售"))
SUP_STATUS=((0,"合作"),(1,"终止"))
class LoginUser(models.Model):
    email=models.EmailField(max_length=20,verbose_name="邮箱")
    password=models.CharField(max_length=50,verbose_name="密码")
    phone_num=models.CharField(max_length=11,verbose_name="手机号",null=True,blank=True)
    age=models.IntegerField(verbose_name="年龄",null=True,blank=True)
    gender=models.IntegerField(default=0,choices=GENDER_STATUS,verbose_name="性别")
    address=models.TextField(verbose_name="地址",null=True,blank=True)
    createtime=models.DateTimeField(auto_now=True,verbose_name="创建时间")
    isDelete=models.IntegerField(default=0,choices=ISDELETE_STATUS,verbose_name="是否删除") #否代表为没有删除,1代表删除

    class Meta:
        db_table="loginuser"
        verbose_name_plural="用户表"

class Supplier(models.Model):
    sup_name=models.CharField(max_length=32,verbose_name="供应商名称")
    sup_country=models.CharField(max_length=32,verbose_name="供应商/国籍",null=True,blank=True)
    sup_province=models.CharField(max_length=32,verbose_name="省/州",null=True,blank=True)
    sup_city=models.CharField(max_length=32,verbose_name="市",null=True,blank=True)
    sup_area=models.CharField(max_length=32,verbose_name="区县",null=True,blank=True)
    sup_address=models.TextField(max_length=32,verbose_name="具体地址",null=True,blank=True)
    sup_phone=models.CharField(max_length=11,verbose_name="手机号")
    sup_tel=models.CharField(max_length=15,verbose_name="座机电话",null=True,blank=True)
    sup_email=models.EmailField(verbose_name="邮箱",null=True,blank=True)
    sup_sex=models.IntegerField(choices=GENDER_STATUS,default=0,verbose_name="性别")
    sup_user=models.CharField(max_length=20,verbose_name="联系人")
    sup_status=models.IntegerField(default=0,choices=SUP_STATUS,verbose_name="是否合作")

    class Meta:
        db_table="supplier"
        verbose_name_plural="供应商表"
    def __str__(self):
        return self.sup_name

class Goods(models.Model):
    Goods_num=models.CharField(max_length=13,verbose_name="商品编号")#商品条形码13位,不足用填充0
    Goods_name=models.CharField(max_length=32,verbose_name="商品名称")
    Goods_price=models.FloatField(verbose_name="销售单价")
    Goods_count=models.IntegerField(verbose_name="商品数量")
    Goods_location=models.CharField(max_length=32,verbose_name="商品产地",null=True,blank=True)
    Goods_safe_date=models.IntegerField(verbose_name="保质期(天)",null=True,blank=True)
    Goods_pro_date=models.DateTimeField(auto_now=True,verbose_name="生产日期")
    Goods_status=models.IntegerField(default=0,choices=GOODS_STATUS,verbose_name="商品状态")
    Goods_inprice=models.FloatField(verbose_name="成本价")
    supplier=models.ForeignKey(to=Supplier,verbose_name="供应商",to_field="id",on_delete=models.CASCADE)


    class Meta:
        db_table="goods"
        verbose_name_plural="商品表"

