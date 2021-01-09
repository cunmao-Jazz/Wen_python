from django.urls import path
from App.views import *
urlpatterns = [
    #首页
    path(r'',home.home,name='index'),
    path(r'home/',home.home,name='home'),
    #购物车
    path(r'cart/',cart.cart,name='cart'),
    #查询当前用户下订单，需要查询是否有选择商品
    path(r'findChoose/',cart.findChoose,name='findChoose'),
    #商品添加到购物车
    path(r'do_cart/',cart.do_cart,name='do_cart'),
    #闪送超市
    #无参路由
    path(r'market/',market.market,name='market'),
    #有参路由
    path(r'market_aegs/<int:categoryid>/<int:childcid>/<int:sort>/',market.market,name='market_args'),
    #我的
    path(r'mine/',mine.mine,name='mine'),
    #注册
    path(r'register/',mine.register,name='register'),
    #ajax注册
    path(r'do_register/',mine.do_register,name='do_register'),
    #登录
    path(r'login/',mine.Login,name='login'),
    #登录功能处理
    path(r'do_login/',mine.do_login,name='do_login'),
    #退出登录
    path(r'logout/',mine.Logout,name='logout'),
    #头像上传
    path(r'upload/',mine.upload,name='upload'),
    # 处理注册功能的路由
    # path(r'do_register/', mine.do_register, name='do_register'),
    # 验证码
    path(r'verifycode/', mine.verifycode, name='verifycode'),
    #地址路由
    path(r'address/',address.address,name='address'),
    #添加地址
    path(r'add_address/',address.add_address,name='add_address'),
    #更改默认地址的路由
    path(r'chang_address/',address.changDefaultAddress,name='chang_address'),
    #更改地址
    path(r'update_address/',address.update_address,name='update_address'),
    #删除地址
    path(r'delete_address/',address.delete_address,name='delete_address'),
    # ---------------------------------------------------------------------
    #订单处理路由地址
    #订单展示
    path(r'show_order/',order.show,name='show_order'),
    #订单支付
    path(r'pay/',order.pay,name='pay'),
    #订单支付后的回调
    path(r'overPay/',order.overPay,name='overPay'),
    #展示购买后的订单
    path(r'show_do_order/',order.show_do_order,name='show_do_order'),
    #删除订单
    path(r'del_order/',order.del_order,name='del_order'),
    #未付款订单
    path(r'no_pay/',order.no_pay,name='no_pay'),
    #未付款订单支付
    path(r'no_pay_pay',order.no_pay_pay,name='no_pay_pay')


]