from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.shortcuts import reverse
from App.models import User


class UserAccountMiddle(MiddlewareMixin):
    def process_request(self, req):
        if req.method == 'POST':
            if req.path == reverse('App:do_register') or req.path == reverse('App:login'):
                userAccount = req.POST.get('userAccount').strip()
                u = User.objects.filter(username=userAccount).first()
                if u:
                    if req.path == reverse('App:do_register'):
                        return JsonResponse({'code': 2, 'err': '该用户已存在'})
                elif req.path == reverse('App:do_login'):
                    return JsonResponse({'code': 1, 'err': '该用户不存在'})