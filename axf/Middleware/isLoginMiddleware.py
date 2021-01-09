from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.shortcuts import reverse
from App.models import User

#必须登录才能访问
class isLoginMiddle(MiddlewareMixin):
    def process_request(self, req):
        if req.method == 'POST' and (req.path == reverse('App:do_cart') or
            req.path == reverse('App:chang_address') or req.path == reverse('App:delete_address')):
            if not req.user.is_authenticated:
                return JsonResponse({'code':1})