from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.shortcuts import reverse
from django.conf import settings
from django.shortcuts import HttpResponse
#文件上传类型的限制
class IconMiddle(MiddlewareMixin):
    def process_request(self, req):
        if req.method == 'POST' and req.path == reverse('App:upload'):
            try:
                suffix = req.FILES.get('file').name.split('.')[-1]
                if suffix not in settings.ALLOWED_FILES:
                    return HttpResponse('该类型文件不支持')
            except:
                return HttpResponse('上传异常')