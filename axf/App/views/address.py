from django.shortcuts import render, HttpResponse, redirect, reverse
from App.models import Address
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
#地址管理
@login_required
def address(req):
    # 查询当前用户的所有地址信息
    u = req.user
    addressData = u.user_address.all()
    count = addressData.count()
    return render(req,'address/address.html',{'addressData':addressData,'count':count})
#添加地址
@login_required
def add_address(req):
    u = req.user
    if req.method == 'GET':
        return render(req,'address/add_address.html')
    elif req.method == 'POST':
        address = req.POST.get('address')
        phone = req.POST.get('phone')
        name = req.POST.get('name')
        state = int(req.POST.get('state'))
        if state == 1:
            #查询用户是否有默认地址 如果有则修改成0 取消默认地址选中
            u.user_address.filter(state=1).update(state=0)
        #将数据写入到数据库中
        Address(user=req.user,address=address,phone=phone,name=name,state=state).save()
        return redirect(reverse('App:address'))

#更改默认地址
def changDefaultAddress(req):
    u = req.user
    if not req.is_ajax():
        return JsonResponse({'code':404})
    try:
        addId = req.POST.get('addid')
        u.user_address.filter(state=1).update(state=0)
        obj = Address.objects.get(id=addId)
        obj.state = 1
        obj.save()
        return JsonResponse({'code': 200})
    except:
        return JsonResponse({'code':500})

#更改默认地址
@login_required
def update_address(req):
    u = req.user
    if req.method == 'GET':
        aid = int(req.GET.get('aid'))
        addressObj = Address.objects.get(id=aid)
        return render(req,'address/update_address.html',{'addressObj':addressObj})
    elif req.method == 'POST':
        address = req.POST.get('address')
        name = req.POST.get('name')
        phone = req.POST.get('phone')
        aid = int(req.POST.get('aid'))
        addressObj = Address.objects.get(id=aid)
        addressObj.address = address
        addressObj.name = name
        addressObj.phone = phone
        addressObj.save()

        return redirect(reverse('App:address'))

#删除送货地址
def delete_address(req):
    u = req.user
    if not req.is_ajax():
        return JsonResponse({'code': 404})
    aid = req.POST.get('aid')
    print(aid)
    count = u.user_address.all().count()
    if count > 1:
        Address.objects.get(id=aid).delete()
        return JsonResponse({'code':3})
    return JsonResponse({'code':2})
