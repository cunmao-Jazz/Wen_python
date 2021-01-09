from django.shortcuts import render,HttpResponse
from App.models import wheel,Nav,Shop,Mustbuy,MainShow
# Create your views here.

def home(req):
    #查询轮播图数据
    whell = wheel.objects.all()
    #nav的数据查询
    nav = Nav.objects.all()
    mustBuy = Mustbuy.objects.all()
    #shop数据
    shop = Shop.objects.all()
    shop1 = shop[0]
    shop2 = shop[1:3]
    shop3 = shop[3:7]
    shop4 = shop[7:]
    #mainshow数据
    mainshow = MainShow.objects.all()
    return render(req,'home/home.html',{'wheel':whell,'nav':nav,
    'mustBuy':mustBuy,'shop1':shop1,'shop2':shop2,'shop3':shop3,'shop4':shop4,'mainshow':
    mainshow})
