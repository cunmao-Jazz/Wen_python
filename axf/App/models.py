from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#自定义用户表
class User(AbstractUser):
    icon = models.CharField(max_length=255,null=True)
    class Meta:
        db_table = 'user'


#创建模型类
#定义一个抽象类
class Common(models.Model):
    img = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    trackid = models.CharField(max_length=10)
    class Meta:
        abstract = True
#轮播图
class wheel(Common):
    class Meta:
        db_table = 'axf_wheel'

#nav
class Nav(Common):
    class Meta:
        db_table = 'axf_nav'

#mustbuy
class Mustbuy(Common):
    class Meta:
        db_table = 'axf_mustbuy'

# shop
class Shop(Common):
    class Meta:
        db_table = 'axf_shop'

# mainShow
class MainShow(Common):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=10)
    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=30)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)
    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=30)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)
    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=30)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)

    class Meta:
        db_table = 'axf_mainshow'

#商品类别表
class FoodTypes(models.Model):
    typeid = models.CharField(max_length=10,verbose_name='类别id')
    typename = models.CharField(max_length=10,verbose_name='类别名称')
    childtypenames = models.CharField(max_length=120,verbose_name='子类别id和名称')
    typesort = models.IntegerField(verbose_name='排序字段')
    class Meta:
        db_table = 'axf_foodtypes'
#商品表
class Goods(models.Model):
    productid = models.CharField(max_length=10,verbose_name='商品id')
    productimg = models.CharField(max_length=100,verbose_name='商品图片')
    productname = models.CharField(max_length=30,verbose_name='商品名称')
    productlongname = models.CharField(max_length=50,verbose_name='商品的长名称')
    isxf = models.BooleanField(verbose_name='是否精选')
    pmdesc = models.BooleanField(verbose_name='是否买一赠一')
    specifics = models.CharField(max_length=10,verbose_name='规格')
    price = models.CharField(max_length=10,verbose_name='价格')
    marketprice = models.CharField(max_length=10,verbose_name='超市价格')
    categoryid = models.CharField(max_length=10,verbose_name='类别id')
    childcid = models.CharField(max_length=10,verbose_name='子类别id')
    childcidname = models.CharField(max_length=10,verbose_name='子类别名称')
    dealerid = models.CharField(max_length=10,verbose_name='详情页id')
    storenums = models.IntegerField(verbose_name='库存')
    productnum = models.IntegerField(verbose_name='销量')
    class Meta:
        db_table = 'axf_goods'

#购物车模型类
class Cart(models.Model):
    #一对多模型关系，一个商品可能会存在多个人的购物车中，每个人的购物车只会存储当场商品的一条数据，但是数量有多个，但是不能超出商品库存
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name='商品一对多关系')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户一对多关系')
    num = models.IntegerField(default=1,verbose_name='购物车商品数量')
    isChoose = models.BooleanField(default=False,verbose_name='商品在购物车中是否选中')
    selectAll = models.BooleanField(default=False,verbose_name='是否全选')
    class Meta:
        db_table = 'axf_cart'

#地址模型类
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_address',verbose_name='一对多')
    address = models.CharField(max_length=200,verbose_name='地址详情')
    phone = models.CharField(max_length=11,verbose_name='手机号码')
    name = models.CharField(max_length=20,verbose_name='接收人')
    state = models.BooleanField(default=False,verbose_name='默认地址')
    isDelete = models.BooleanField(default=False,verbose_name='是否删除')
    class Meta:
        db_table = 'axf_address'

#订单模型类
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户外键')
    address = models.ForeignKey(Address,on_delete=models.CASCADE,verbose_name='地址外键')
    money = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='订单总金额')
    message = models.CharField(max_length=100,verbose_name='买家留言')
    createTime = models.DateTimeField(auto_now_add=True,verbose_name='下单时间')
    orderId = models.CharField(max_length=64,verbose_name='订单ID')
    state = models.BooleanField(default=False,verbose_name='订单状态') #1 支付 0 未支付
    isDelete = models.BooleanField(default=False,verbose_name='是否删除')
    class Meta:
        db_table = 'axf_order'

#订单详情
class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='订单外键')
    goodsImg = models.CharField(max_length=100,verbose_name='商品图片')
    goodsName = models.CharField(max_length=50,verbose_name='商品名称')
    price = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='商品单价')
    num = models.IntegerField(default=1,verbose_name='商品数量')
    total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='总价')
    class Meta:
        db_table = 'axf_orderDetail'