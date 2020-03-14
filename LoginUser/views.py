from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from LoginUser.models import *

# Create your views here.

#密码加密
import hashlib
def setpassword(pwd):
    md5=hashlib.md5()
    md5.update(pwd.encode())
    result=md5.hexdigest()
    return result

#登录装饰器
def loginvalid(func):
    def inner(request,*args,**kwargs):
        #根据登录设置的
        c_email=request.COOKIES.get("email")
        s_email=request.session.get("email")
        if c_email and s_email and c_email==s_email:
            return  func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/login/")#重定向到登录页面
    return  inner

#注册页面
def register(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        repassword=request.POST.get("repassword")
        if email and password and password==repassword:
            params={"email":email,"password":setpassword(password)}
            user_obj=LoginUser.objects.create(**params)
            if user_obj:
                return HttpResponseRedirect("/login/")
            else:
                message="用户注册失败"
                return render(request, "register.html",locals())
        else:
            message="都不能为空,且密码两次一样"
            return render(request, "register.html",locals())
    return render(request,"register.html",locals())

#ajax判断用户是否注册(利用ajax去判断用户是否已经注册了)
def ajax_register(request):
    email = request.GET.get("email")
    print("email:"+email)
    if email:
        flag = LoginUser.objects.filter(email=email).exists()
        if flag:
            ## True  账号存在
            message = "邮箱已注册，请换一个"
        else:
            ## flase  账号不存在
            # message = "账号不存在"
            message = ""
    else:
        message = "邮箱不能为空"
    return HttpResponse(message)
#ajax判断密码两次输入的是否一样
def ajax_pregister(request):
    result = {"code": 10000, "msg": ""}
    password = request.POST.get("password")

    repassword = request.POST.get("repassword")
  # print(request.POST)

    if repassword and password and repassword==password:
         result = {"code": 10000, "msg": ""}
    else:
        result = {"code": 10001, "msg": "密码不为空或两次必须一样"}
    return JsonResponse(result)


#模板页面
def base(request):
    return render(request,"base.html")
#用户登录
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email and password:
            user_obj=LoginUser.objects.filter(email=email,password=setpassword(password)).first()
            if user_obj:
                response=HttpResponseRedirect("/")
                response.set_cookie("email",user_obj.email)
                request.session["email"]=user_obj.email
                return response
            else:
                message = "邮箱或密码不正确"
                return render(request, "login.html", locals())
        else:
            message = "邮箱和密码不能为空"
            return render(request, "login.html", locals())
    return render(request,"login.html")

#用户退出登录
def loginout(request):
    response=HttpResponseRedirect("/login/")
    response.delete_cookie("email")
    del request.session["email"]
    return response
#首页
from CeleryTask.tasks import TaskTest,MyPrint #任务方法
from django.views.decorators.cache import cache_page #缓存需要的包
#
@cache_page(60*15)#代表15分钟
@loginvalid
def index(request):
    #发布任务
    TaskTest.delay()
    #发布任务
    MyPrint.delay(100)#里面是参数
    print("helloword")#第一次用了缓存，然后加入进去这个，那么读取的时候就读取不到这个，因为直接取了缓存拿
    return render(request,"index.html",locals())

#商品信息(路由在子路由LoginUser中)加载商品信息
#分页用到的包
from django.core.paginator import Paginator
def goods_list(request,status=3,page=1):
    #返回到前端的一个标题值
    goods_title=""
    if status=="0" or status=="1":# 0在售商品,1是停售
        if status=="0":
            goods_title="在售商品"
        else:
            goods_title="停售商品"
        goods_obj=Goods.objects.filter(Goods_status=status).order_by("-id")
    else:
        goods_title="全部商品"
        goods_obj=Goods.objects.all().order_by("-id")
    if goods_obj:
        paginator=Paginator(goods_obj,8)
        page_obj=paginator.page(page)
        print(page_obj)#代表每一页的数据对象
    else:
        message="未找到相关记录"
    return render(request,"goods_list.html",locals())

#商品的上架和下架功能实现,都是修改状态
def goods_status(request,id,status):
    #找到这个数据
    # print(request.META["HTTP_REFERER"])#获取的是当前页面地址
    goods_obj=Goods.objects.get(id=id)
    if status=="up":#点击上架说明原来是下架的（下架的为1）
        goods_obj.Goods_status=0
        goods_obj.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else: #下架
        goods_obj.Goods_status=1
        goods_obj.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

#修改商品
def updategoods(request,id):
    #查询所有的供应商信息
    sup_obj=Supplier.objects.all()
    # back_ulr=request.META["HTTP_REFERER"]
    try:
        back_ulr = request.META["HTTP_REFERER"]
    except:
        # back_ulr=request.META["PATH_INFO"]
        # print(request.META["HTTP_HOST"])
        pass
    u_goods_obj=Goods.objects.get(id=id)#获取id对应的商品信息
    #get就是读取数据
    if request.method=="POST":
        # 修改和保存数据
        try:
            u_goods_obj.Goods_num=request.POST.get("goodsnum") #商品编码
            u_goods_obj.Goods_name = request.POST.get("goodsname") #名称
            goodsp = request.POST.get("goodsprice") #销售价
            u_goods_obj.Goods_price=str(goodsp).split("$")[1]
            u_goods_obj.Goods_count = request.POST.get("goodscount") #数量
            u_goods_obj.Goods_pro_date = request.POST.get("goodsdate") #生产日期
            u_goods_obj.Goods_status=request.POST.get("radiostatus") #商品状态
            select_g=request.POST.get("select_g") #供应商
            u_goods_obj.supplier_id=str(select_g).split(":")[0]
            goodsip = request.POST.get("goodsinp") #进价
            u_goods_obj.Goods_inprice=str(goodsip).split("$")[1]
            u_goods_obj.Goods_location = request.POST.get("goodscity") #产地
            u_goods_obj.Goods_safe_date = request.POST.get("goodssafe") #保质期
            u_goods_obj.save()
            message="修改数据成功"#代表数据成功
        except:
            message="修改数据失败"#数据失败
        return render(request, "updategoods.html", locals())
    else:
        if u_goods_obj:
            return render(request, "updategoods.html", locals())
        else:
            return HttpResponseRedirect("没有找到相关数据")

#商品进货


#个人中心
def person(requst):
    if requst.is_ajax():#判断是否是ajax方法
        pass
    person_tilet="个人中心"
    return render(requst,"person.html",locals())

#添加商品信息
# import random
# def add_goods(request):
#     goods_name="大葱、芹菜、蒜苗、小葱、菠菜、韭菜、西芹、南瓜、冬瓜、黄瓜、辣椒、花菜、莲藕、木耳、蒜苔、白菜、青菜、包菜、生菜、菠菜、韭菜、韭黄、蒜苗、芹菜、水芹、苦菊、茼蒿、苋菜、香椿、冲菜、贡菜、芥兰、荠菜、茴香、蕹菜、芥菜、莼菜、发菜、海带、紫菜、米苋、芜荽、油菜、辣根、萝卜、大葱、" \
#                "小葱、洋葱、生姜、洋姜、莲菜、蒜薹、莴笋、山药、芋头、魔芋、土豆、红薯、凉薯、地瘤、芦笋、竹笋、牛蒡、茭白、荞头、芦笋、荸荠、菱角、蕨菜、莴苣、慈姑、芜普、豆薯、百合、莲藕、姜芽、豆苗、芥蓝、辣椒、菜椒、青椒、尖椒、甜椒、南瓜、冬瓜、苦瓜、乳瓜、黄瓜、丝瓜、菜瓜、胡瓜、瓠瓜、菜瓜、番茄、茄子、芸豆、豇豆、豌豆、架豆、刀豆、扁豆、青豆、毛豆、蛇豆、玉米、蚕豆、菜豆、眉豆、蛇瓜、木耳、银耳、地耳、石耳、平菇、草菇、口蘑、香菇、竹荪、红萝卜、西红柿、大白菜、小平菇、金针菇、紫包菜、" \
#                "杏鲍菇、青辣椒、四季豆、绿豆芽、黄豆芽、西兰花、雪里红、大白菜、小白菜、小青菜、紫甘蓝、韭菜花、龙须菜、菊花脑、油麦菜、人参菜、黄秋葵、富贵菜、韭菜薹、番薯叶、紫背菜、空心菜、娃娃菜、苔干叶、山蛰菜、马齿苋、金花菜、苜蓿菜、木耳叶、海白菜、瓢儿菜、罗汉菜、白罗卜、胡罗卜、水罗卜、桔梗丝、宝塔菜、鱼腥草、" \
#                "鲜榨菜、金针菜、石刁柏、大头菜、豌豆芽、香椿芽、萝卜芽、荞麦芽、花生芽、黄豆芽、绿豆芽、花椰菜、金针菜、青花菜、紫菜蔓、 朝鲜蓟、朝天椒、螺丝椒、金南瓜、西葫芦、佛手瓜、四棱豆、玉米尖、猴头菇、金针菇、鸡腿菇、凤尾菇、茶树菇、杏鲍菇、秀珍菇、猪肚菇、裙带菜、芽甘蓝、子持甘蓝、羽衣甘蓝、紫背天葵、结球白菜、" \
#                "广东菜芯、结球甘蓝、结球莴苣、包心芥菜、大叶香菜、小叶香菜、芜菁甘蓝、根用甜菜、球茎甘蓝、灯笼辣椒"
#     goods_name=goods_name.split("、")
#     goods_location="重庆、哈尔滨、拉萨、南宁、昆明、长春、呼和浩特、杭州、北京、石家庄、乌鲁木齐、兰州、沈阳、成都、福州、天津、长沙、合肥、西安、银川、武汉、济南、贵阳、西宁、郑州、广州、南昌、太原、南京、上海、海口、香港、台北、澳门"
#     goods_location = goods_location.split("、")
#     for i,j in enumerate(range(80),1):
#         goods=Goods()
#         goods.Goods_num=str(i).zfill(13)
#         goods.Goods_name=random.choice(goods_location)+random.choice(goods_name)
#         goods.Goods_price=round(random.random()*10,2)
#         goods.Goods_count=random.randint(1,100)
#         goods.Goods_location=random.choice(goods_location)
#         goods.Goods_safe_date=random.randint(1,100)
#         goods.Goods_inprice=round(random.random()*6,2)
#         goods.supplier_id=random.choice([1,2])
#         goods.save()
#     return  HttpResponse("增加成功")


#restful
from .serializers import GoodsSerializer
from rest_framework import viewsets,mixins
class GoodsViews(mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Goods.objects.all().order_by("id")
    serializer_class = GoodsSerializer


# 记得要导包啊
from rest_framework import viewsets, filters, pagination


class PageSet(pagination.PageNumberPagination):
    # 每页显示多少个
    page_size = 8
    # 默认每页显示3个


page_size_query_param = "size"
# 最大页数
max_page_size = 10
# 获取页码数的
page_query_param = "page"


class GoodsViewSet(viewsets.ModelViewSet):
    # 指定结果集并设置排序
    queryset = Goods.objects.all().order_by('id')
    # 指定序列化的类
    serializer_class = GoodsSerializer
    #指定分页配置
    pagination_class = PageSet


def phone(request):
    num=request.POST.get("phone")
    if request.method=="POST":
        if len(str(num))!=11:
            message="手机号必须是11位"
    return render(request,"phone.html",locals())

#生成验证码
from PIL import  Image,ImageDraw,ImageFont
import random
import io
def verifycode(request):
    #定义变量,用户画背景色,宽,高
    bgcolor=(random.randrange(20,100),random.randrange(20,100),random.randrange(20,100))
    print(bgcolor)
    width,height=100,35
    #创建画布对象
    im=Image.new("RGB",(width,height),bgcolor)
    #创建画笔（关联画布）
    draw=ImageDraw.Draw(im)
    #调用画笔的point()绘制噪点
    for i in range(0,100):
        xy=(random.randrange(0,width),random.randrange(0,height))#xy坐标随机值
        fill=(random.randrange(0,255),255,random.randrange(0,255))#颜色的随机值
        draw.point(xy,fill=fill)#绘制噪点
    #定义验证码的备选值
    strcode="1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #选择四个作为验证码
    select_code=[random.choice(strcode) for i in range(0,4)]
    #构造字体对象（字体，大小）
    ifont=ImageFont.truetype(r"C:\Windows\Fonts\MOD20.TTF",24)
    #构造字体颜色(随机)和绘制字
    ncode=""
    for f in range(0,len(select_code)):
        #字体颜色
        fcolor=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        draw.text((25*(f)+10,2),select_code[f],font=ifont,fill=fcolor)
        ncode+=select_code[f]
    #释放画笔
    del draw
    #存入session,用于做进一步验证
    request.session["verifycode"]=ncode
    #存入内存文件
    buf=io.BytesIO()
    #将图片保存在内存中,文件类型为png
    im.save(buf,"png")
    #将内存中的图片数据返回给客户端,MIME类型为图片png

    return HttpResponse(buf.getvalue(),"image/png")

def test(request):
    if request.method=="POST":
        ncode=request.POST.get("ncode")
        # ycode=request.session["verifycode"]
        ycode=request.session.get("verifycode")
        print(ycode)
        if ncode==ycode:
            message="验证码正确"
        else:
            message="错误验证码"
    return render(request,"testcode.html",locals())


