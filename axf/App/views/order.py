from django.shortcuts import render,HttpResponse,redirect,reverse
from django.contrib.auth.decorators import login_required
import uuid,hashlib
from App.models import Order,OrderDetail,Address
from django.db import transaction
from alipay import AliPay
from django.conf import settings
from django.http import JsonResponse
#订单展示
@login_required
def show(req):
    u = req.user
    #查询该用户选择要下单的商品
    orderData =  req.user.cart_set.filter(isChoose=True)
    #查询该用户的默认地址
    address = u.user_address.filter(state=True).first()
    #判断是否有默认地址
    if not address:
        #如果没有默认地址获取用户的第一条地址
        address =  u.user_address.all().first()
        #如果当前用户没有地址，重定向到添加地址
        if not address:
            return redirect(reverse('App:add_address'))
    totalMoney = 0 #当前订单金额的初始值
    for goods in orderData:
       totalMoney +=  goods.num * eval(goods.goods.price)
    return render(req,'order/show_order.html',{'orderData':orderData,'address':address,
                                               'totalMoney':'%.2f'%(totalMoney)})


#支付路由
@login_required
def pay(req):
    if req.method == 'POST':
        message = req.POST.get('message') #获取留言
        address = req.POST.get('address') #获取地址id
        totalMoney = req.POST.get('totalMoney') #订单金额
        #生成唯一的订单id号
        uuidStr = str(uuid.uuid4())
        md5 = hashlib.md5(uuidStr.encode('utf-8'))
        orderId = md5.hexdigest()
        try:
            # 添加事务处理，异常回滚
            with transaction.atomic():
                # 订单模型类保存
                order = Order(user=req.user, address=Address.objects.get(id=address), money=totalMoney, message=message,
                          orderId=orderId)
                order.save()
                # 查询购物车中用户选中的商品
                cartGoods = req.user.cart_set.filter(isChoose=True)
                for goods in cartGoods:
                    # 减去用户下单商品的库存数
                    goodsNum = goods.goods
                    goodsNum.storenums -= goods.num
                    goodsNum.save()
                    # 保存订单商品模型的详细信息
                    OrderDetail(order=order, goodsImg='1.jpg',
                            goodsName=goodsNum.productname, price=goodsNum.price, num=goods.num,
                            total=goods.num * eval(goodsNum.price)).save()
        except:
            return HttpResponse('<meta http-equiv="Refresh" content="3;url='+reverse('App:cart')+'" />当前业务繁忙,'
             ' 清稍后再试 3s后跳转')
        #进行支付处理
        alipay = AliPay(
            appid=settings.APP_ID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=settings.APP_PRIVATE_KEY_STRING,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=settings.APP_PRIVATE_KEY_STRING,
            sign_type="RSA2",# RSA 或者 RSA2
            debug = False,  # 默认False
        )

        subject = "订单"

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=orderId,
            total_amount=totalMoney,
            subject=subject,
            return_url="http://121.4.50.115:7800/overPay/",
            notify_url=""  # 可选, 不填则使用默认notify url
        )
        return redirect('https://openapi.alipaydev.com/gateway.do?'+ order_string)

#支付成功的回调
@login_required
def overPay(req):
    #获取订单ID
    orderId = req.GET.get('out_trade_no')
    order = Order.objects.get(orderId=orderId)
    order.state = True
    order.save()
    return redirect(reverse('App:show_do_order'))

#订单展示
@login_required
def show_do_order(req):
    #查询未删除订单
    order = req.user.order_set.filter(isDelete=False)
    #查询订单详情
    for o in order:
        o.detail =  o.orderdetail_set.all()
    return render(req,'order/show_do_order.html',{'order':order})
#删除订单
def del_order(req):
    if not req.user.is_authenticated:
        return JsonResponse({'code': 2})
    if req.is_ajax():
        try:
            orderId = req.GET.get('orderId')
            o = Order.objects.get(orderId=orderId)
            o.isDelete = True
            o.save()
            return JsonResponse({'code': 0})
        except:
            return JsonResponse({'code':1})

# 查询未付款的订单
@login_required
def no_pay(req):
    order = req.user.order_set.filter(state=False,isDelete=False)
    for o in order:
        o.detail = o.orderdetail_set.all()
    return render(req,'order/no_pay.html',{'order':order})

@login_required
def no_pay_pay(req):
    orderId = req.GET.get('orderId')
    totalMoney = req.GET.get('totalMoney')
    # 进行支付处理
    alipay = AliPay(
        appid=settings.APP_ID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=settings.APP_PRIVATE_KEY_STRING,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=settings.APP_PRIVATE_KEY_STRING,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False,  # 默认False
    )

    subject = "订单"

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=orderId,
        total_amount=totalMoney,
        subject=subject,
        return_url="http://121.4.50.115:7800/overPay/",
        notify_url=""  # 可选, 不填则使用默认notify url
    )
    return redirect('https://openapi.alipaydev.com/gateway.do?' + order_string)