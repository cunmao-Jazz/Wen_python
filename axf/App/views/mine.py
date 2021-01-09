from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, reverse
from App.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout,authenticate
from django.conf import settings
import os
import uuid
from PIL import Image
import io


def mine(req):
    return render(req, 'mine/mine.html')


# 注册
"""
def register(req):
    if req.method == 'GET':
        return render(req, 'mine/register.html')
    else:
        try:
            userAccount = req.POST.get('userAccount')
            userpass = req.POST.get('userpass')
            email = req.POST.get('email')
            firstname = req.POST.get('firstname')
            yzm = req.POST.get('yzm')
            if yzm.lower() != req.session.get('verify').lower():
                return HttpResponse('请输入正确的验证码')
            u = User.objects.filter(username=userAccount).first()
            if u:
                return HttpResponse('当前用户已存在')
            User.objects.create_user(userAccount, email, userpass, first_name=firstname)
        except:
            return HttpResponse('抱歉 注册失败')
        return redirect(reverse('App:login'))
"""
def register(req):
    if req.method == 'GET':
        return render(req, 'mine/register.html')

def do_register(req):
        if not req.is_ajax():
            return JsonResponse({'code': 404})
        userAccount = req.POST.get('userAccount').strip()
        userpass = req.POST.get('userpass')
        email = req.POST.get('email')
        firstname = req.POST.get('firstname')
        try:
            User.objects.create_user(userAccount, email, userpass, first_name=firstname)
        except:
            return JsonResponse({'code':3,'err':'注册失败'})
        return JsonResponse({'code':0})
# 登录
def Login(req):
        next = 0
        url = req.GET.get('next')
        if url:
            next = reverse('App:'+ url.strip('/'))
        return render(req,'mine/login.html',{'next':next})


def do_login(req):
    if not req.is_ajax():
        return JsonResponse({'code':404})
    #接受用户数据
    userAccount = req.POST.get('userAccount')
    userpass = req.POST.get('userpass')
    u = authenticate(username=userAccount,password=userpass)
    #进行用户认证
    if not u:
        return JsonResponse({'code':2,'err':'密码不正确'})
    login(req,u) # 维持用户状态

    return JsonResponse({'code':0})
#退出登录
def Logout(req):
    logout(req)
    return redirect(reverse('App:home'))

def upImage(fileName,buf,w=100,h=100):
    import oss2
    # 云存储
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
    auth = oss2.Auth(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'wen-new')
    bucket.put_object(fileName, buf.getvalue())
    style = 'image/resize,m_fixed,w_{},h_{}'.format(w,h)
    url = bucket.sign_url('GET', fileName, 60 * 60 * 24 * 360 * 50, params={'x-oss-process': style})
    return url

@login_required
def upload(req):
    if req.method == 'GET':
        return render(req,'mine/upload.html')
    elif req.method == 'POST':
        file = req.FILES.get('file')
        print(file.name)
        suffix = file.name.split('.')[-1]
        fileName = str(uuid.uuid4())+'.'+suffix
        try:
            img = Image.open(file)
            buf = io.BytesIO()
            img.save(buf,'png')
            url = upImage(fileName,buf)

            #将头像保存再数据库
            u = req.user
            u.icon = url
            u.save()
            return redirect(reverse('App:mine'))
        except:
            return HttpResponse('文件上传失败')



def verifycode(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    # 构造字体对象
    font = ImageFont.truetype(os.path.join(settings.FONTS_DIRS,'ADOBEARABIC-BOLDITALIC.OTF'), 40)
    # 构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verify'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')







