
from django.shortcuts import redirect
from django.urls import reverse
import re

class ShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("ShopMiddleware")

    def __call__(self, request):
        path = request.path
        print("url:",path)

        
        urllist = ['/myadmin/login','/myadmin/logout','/myadmin/dologin']
        
        if re.match(r'^/myadmin',path) and (path not in urllist):
            
            if 'adminuser' not in request.session:
                
                return redirect(reverse("myadmin_login"))
                #pass
        if re.match(r'^/web',path):
            
            if 'webuser' not in request.session:
              
                return redirect(reverse("web_login"))

        response = self.get_response(request)
        
        return response