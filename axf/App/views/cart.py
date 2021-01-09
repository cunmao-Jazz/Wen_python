from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse
from App.models import Cart,Goods
from django.http import JsonResponse

#购物车
@login_required
def cart(req):
    #获取当前登录用户中所有购物车商品
    cartDate = req.user.cart_set.all()
    #计算当前选中商品的总金额
    totalMoney = 0
    cartChoose = cartDate.filter(isChoose=True)
    for choose in cartChoose:
        totalMoney += eval(choose.goods.price) * choose.num
    # 全选判断值
    cartfirst = req.user.cart_set.all().first()

    return render(req,'cart/cart.html',{'cartDate':cartDate,'totalMoney':'%.2f'%totalMoney,'cartfirst':cartfirst})

def do_cart(req):
    if not req.is_ajax():
        return JsonResponse({'code':404})
    #接受数据
    goodsId = req.POST.get('goodsId') #商品id
    state = int(req.POST.get('state')) #状态 0 - 1 +

    Bool = True #购物车中商品是否选中状态默认值
    #当前用户
    u = req.user

    #获取传递过来的商品id的商品对象
    goodObj = Goods.objects.filter(id=goodsId).first()
    #查询出当前用户的购物车中这个商品的购物车数据
    cartObj = req.user.cart_set.filter(goods=goodObj)
    cartObjExists = cartObj.exists()
    #计算购物车中选中的商品的金额
    totaMoney = 0
    cart = None
    if cartObjExists:
        cart = cartObj.first()
    num = 1
    if state == 0:
        if cartObjExists:
            num = cart.num
            num -=1
            if num > 0:
                cart.num = num
                cart.save()
            else:
                cart.delete() #删除购物车中该商品
        else:
            num = 0
    elif state == 1:
        if cartObjExists: #判断商品是否在购物车中
            num = cart.num #当前商品在购物车中的数量
            num +=1
            #判断商品在购物车中的数量，是否大于商品库存量
            if num >= goodObj.storenums:
                num = goodObj.storenums

            cart.num = num
            cart.save()
        else: #不存在购物车中，把商品写入购物车中
            Cart(goods=goodObj,user=u).save() #保存到购物车中
    #当state为2时，判断商品的选中/未选中
    elif state == 2:
        Bool = not cart.isChoose
        cart.isChoose = Bool
        cart.save()
    #当state为3时,判断是否为全选
    elif state == 3:
        cartall = u.cart_set.all()
        cartfirstall = cartall.first().selectAll
        Bool = not cartfirstall

        for all in cartall:
            all.selectAll = Bool
            all.isChoose = Bool
            all.save()
    #计算当前用户选中的商品金额
    cartChoose = u.cart_set.filter(isChoose=True)
    for choose in cartChoose:
        totaMoney += choose.num * eval(choose.goods.price)
    return JsonResponse({'code':200,'num':num,'totaMoney':'%.2f'%totaMoney,'Bool':Bool})


#处理验证用户是否有选中商品下订单
def findChoose(req):
    if req.is_ajax():
        bool = req.user.cart_set.filter(isChoose=True).exists()
        return JsonResponse({'data':bool})

