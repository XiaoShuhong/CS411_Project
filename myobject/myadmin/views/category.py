from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.
from myadmin.models import Category, Shop
from django.http import JsonResponse

def index(request,pIndex=1):
  
    umod = Category.objects
    ulist = umod.filter(status__lt=9)
    mywhere=[]
    
    kw = request.GET.get("keyword",None)
    if kw:
        ulist = ulist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
     
    status = request.GET.get('status','')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status="+status)
        
    ulist = ulist.order_by("id")
    
    pIndex = int(pIndex)
    page = Paginator(ulist,10) 
    maxpages = page.num_pages 
    
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) 
    plist = page.page_range 

   
    for vo in list2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name

    context = {"categorylist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/category/index.html",context)

def add(request):
    
    #获取当前所有店铺
    slist = Shop.objects.values("id",'name')
    context = {"shoplist":slist}
    return render(request,"myadmin/category/add.html",context)
    # return render(request,"myadmin/category/add.html")
def insert(request):
    
    try:
        ob = Category()
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d")
        ob.update_at = datetime.now().strftime("%Y-%m-%d")
        ob.save()
        context = {'info':"Insert Success"}
    except Exception as err:
        print(err)
        context = {'info':"Insert Error"}
    return render(request,"myadmin/info.html",context)

def delete(request,cid=0):
  
    try:
        ob = Category.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d")
        ob.save()
        context = {'info':"Delete Success"}
    except Exception as err:
        print(err)
        context = {'info':"Delete Error"}
    return render(request,"myadmin/info.html",context)

def edit(request,cid=0):
   
    try:
        ob = Category.objects.get(id=cid)
        context = {'category':ob}
        slist = Shop.objects.values("id",'name')
        context["shoplist"] = slist
        return render(request,"myadmin/category/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Edit Error"}
        return render(request,"myadmin/info.html",context)

def update(request,cid):
  
    try:
        ob = Category.objects.get(id=cid)
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d")
        ob.save()
        context = {'info':"Update Success"}
    except Exception as err:
        print(err)
        context = {'info':"Update Error"}
    return render(request,"myadmin/info.html",context)

def loadCategory(request,sid):
    clist = Category.objects.filter(status__lt=9,shop_id=sid).values("id","name")
    return JsonResponse({'data':list(clist)})