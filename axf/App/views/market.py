from django.shortcuts import render,HttpResponse
from App.models import FoodTypes,Goods

def market(req,categoryid=104749,childcid=0,sort=0):
    foodTypes = FoodTypes.objects.all()
    goodsData = Goods.objects.filter(categoryid=categoryid)
    #判断子类别
    if childcid:
        goodsData = goodsData.filter(childcid=childcid)

    #进行商品排序
    if sort == 1:
        goodsData = goodsData.order_by('-productnum')
    elif sort == 2:
       goodsData = goodsData.order_by('price')

    elif sort == 3:
        goodsData = goodsData.order_by('-price')

    #类别查询 子类别用于展示和查询
    typeList = []

    childTypeData = foodTypes.filter(typeid=categoryid).first()
    childTypeList = childTypeData.childtypenames.split('#')
    #循环迭代当前的子类别列表数据
    for t in childTypeList:
        typeList.append(t.split(':'))

    for row in goodsData:
        num = 0
        #判断当前用户是否登录 登录则查询出商品在购物车中的数量
        if req.user.is_authenticated:
            cartObj = req.user.cart_set.filter(goods=row.id).first()
            if cartObj:
                num = cartObj.num
        row.num = num
    return render(req,'market/market.html',{'foodTypes':foodTypes,'goodsData':goodsData,
    'typeList':typeList,'categoryid':categoryid,'childcid':childcid,'sort':sort})