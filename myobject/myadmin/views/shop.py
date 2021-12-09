from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import time
# Create your views here.
from myadmin.models import Shop

def index(request,pIndex=1):
    smod = Shop.objects
    slist = smod.filter(status__lt=9)
    mywhere=[]
    kw = request.GET.get("keyword",None)
    if kw:
        slist = slist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    status = request.GET.get('status','')
    if status != '':
        slist = slist.filter(status=status)
        mywhere.append("status="+status)
        
    slist = slist.order_by("id")

    pIndex = int(pIndex)
    page = Paginator(slist,5) 
    maxpages = page.num_pages 
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) 
    plist = page.page_range 
    context = {"shoplist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/shop/index.html",context)

def add(request):
    return render(request,"myadmin/shop/add.html")
    

def insert(request):
    try:
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            return HttpResponse("No Picture")
        cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/"+cover_pic,"wb+")
        for chunk in myfile.chunks():     
            destination.write(chunk)  
        destination.close()

        myfile = request.FILES.get("banner_pic",None)
        if not myfile:
            return HttpResponse("No logo")
        banner_pic = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/"+banner_pic,"wb+")
        for chunk in myfile.chunks():     
            destination.write(chunk)  
        destination.close()

        ob = Shop()
        ob.name = request.POST['name']
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d")
        ob.update_at = datetime.now().strftime("%Y-%m-%d")
        ob.save()
        context = {'info':"Insert Success"}
    except Exception as err:
        print(err)
        context = {'info':"Insert Error"}
    return render(request,"myadmin/info.html",context)

def delete(request,sid=0):
    try:
        ob = Shop.objects.get(id=sid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d")
        ob.save()
        context = {'info':"Delete Success"}
    except Exception as err:
        print(err)
        context = {'info':"Delete Error"}
    return render(request,"myadmin/info.html",context)


def edit(request,sid=0):
    try:
        ob = Shop.objects.get(id=sid)
        context = {'shop':ob}
        return render(request,"myadmin/shop/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Edit Error"}
        return render(request,"myadmin/info.html",context)
   
def update(request,sid):
    try:
        ob = Shop.objects.get(id=sid)
        ob.name = request.POST['name']
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d")
        ob.save()
        context = {'info':"Update Success"}
    except Exception as err:
        print(err)
        context = {'info':"Update Error"}
    return render(request,"myadmin/info.html",context)
    