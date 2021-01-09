from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.shortcuts import reverse

class YZMMiddle(MiddlewareMixin):
    def process_request(self, req):
        if req.method == 'POST' and req.path == reverse('App:do_register'):
            yzm = req.POST.get('yzm')
            print(yzm)
            print(req.session.get('verify').lower())
            if yzm.lower() != req.session.get('verify').lower():
                return JsonResponse({'code': 1, 'err': '验证码错误'})