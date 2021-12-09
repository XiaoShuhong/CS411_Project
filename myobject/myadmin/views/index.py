from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse 
# Create your views here.
from myadmin.models import User


def index(request):
    return render(request,'myadmin/index/index.html')


def login(request):
    return render(request,'myadmin/index/login.html')


def dologin(request):
    # # return render(request,'myadmin/index/index.html')
    # try:
    #     user = User.objects.get(uername=request.POST['username'])
    # except Exception as err:
    #     print(err)
    #     context={"Error:Account notexist or password error"}
    # return render(request,'myadmin/index/login.html',context)

    try:
       
        user = User.objects.get(username=request.POST['username'])
        if user.status == 6: 
            
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['pass']+user.password_salt 
            md5.update(s.encode('utf-8')) 
            if user.password_hash == md5.hexdigest(): 
                print('Successfully Login in')
               
                request.session['adminuser'] = user.toDict()
                
                return redirect(reverse("myadmin_index"))
            
            else:
                context = {"info":"Wrong password"}
        else:
            context = {"info":"Invalid Account"}
    except Exception as err:
        print(err)
        context = {"info":"Account not exist"}
    return render(request,"myadmin/index/login.html",context)


def logout(request):
    # return render(request,'myadmin/index/index.html')
    del request.session['adminuser']
    return redirect(reverse("myadmin_login"))
