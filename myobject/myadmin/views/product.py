from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
import time,os
# Create your views here.
from myadmin.models import Product, Category, Shop
from django.db import connection

def index(request,pIndex=1):
    umod = Product.objects
    ulist = umod.filter(status__lt=9)
    mywhere=[]

    kw = request.GET.get("keyword",None)
    if kw:
        resturant_name,category=kw.split(",")
        # print(resturant_name,category)
        with connection.cursor() as cursor:
            insert_stmt=(
                "select product.id,shop.name,product.category_id,product.cover_pic,product.name,product.price,product.status,product.create_at from product join shop on product.shop_id = shop.id where product.category_id = %s and product.id in (select product.id  from product  join shop  on product.shop_id = shop.id where shop.name = %s)"
            )
            data=(str(category),resturant_name)
            cursor.execute(insert_stmt,data)
            rows_all=cursor.fetchall()
            kwlist=[]
            for row in rows_all:
                kw_dict={}
                kw_dict['id']=row[0]
                kw_dict['shopname']=row[1]
                kw_dict['categoryname']=row[2]
                kw_dict['cover_pic']=row[3]
                kw_dict['name']=row[4]
                kw_dict['price']=row[5]
                kw_dict['status']=row[6]
                kw_dict['create_at']=row[7]
                kwlist.append(kw_dict)
        cursor.close()


        # ulist = ulist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
  
    # cid = request.GET.get("category_id",None)
    # if cid:
    #     ulist = ulist.filter(category_id=cid)
    #     mywhere.append('category_id='+cid)
   
    # status = request.GET.get('status','')
    # if status != '':
    #     ulist = ulist.filter(status=status)
    #     mywhere.append("status="+status)
    
    if kw:
        pIndex = int(pIndex)
        page = Paginator(kwlist,10) 
        maxpages = page.num_pages
    else:

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

    if not kw:
        for vo in list2:
            sob = Shop.objects.get(id=vo.shop_id)
            vo.shopname = sob.name
            cob = Category.objects.get(id=vo.category_id)
            vo.categoryname = cob.name

    context = {"productlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/product/index.html",context)




def add(request):
   
    slist = Shop.objects.values("id",'name')
    context = {"shoplist":slist}
    return render(request,"myadmin/product/add.html",context)

def insert(request):
   
    try:
       
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            return HttpResponse("No picture")
        cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/uploads/product/"+cover_pic,"wb+")
        for chunk in myfile.chunks():       
            destination.write(chunk)  
        destination.close()
        
        ob = Product()
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic = cover_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d")
        ob.update_at = datetime.now().strftime("%Y-%m-%d")
        ob.save()
        context = {'info':"Insert Success"}
    except Exception as err:
        print(err)
        context = {'info':"Insert Error"}
    return render(request,"myadmin/info.html",context)

def delete(request,pid=0):
    
    try:
        ob = Product.objects.get(id=pid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d")
        ob.save()
        context = {'info':"Delete Success"}
    except Exception as err:
        print(err)
        context = {'info':"Delete Error"}
    return render(request,"myadmin/info.html",context)

def edit(request,pid=0):
    
    try:
        ob = Product.objects.get(id=pid)
        context = {'product':ob}
        slist = Shop.objects.values("id",'name')
        context["shoplist"] = slist
        return render(request,"myadmin/product/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Edit Error"}
        return render(request,"myadmin/info.html",context)

def update(request,pid):
    
    try:
        
        oldpicname = request.POST['oldpicname']
        
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            cover_pic = oldpicname
        else:
            cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
            destination = open("./static/uploads/product/"+cover_pic,"wb+")
            for chunk in myfile.chunks():     
                destination.write(chunk)  
            destination.close()

        ob = Product.objects.get(id=pid)
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic = cover_pic
        ob.update_at = datetime.now().strftime("%Y-%m-%d")
        ob.save()
        context = {'info':"Update Success"}

        if myfile:
            os.remove("./static/uploads/product/"+oldpicname)

    except Exception as err:
        print(err)
        context = {'info':"Update Error"}
        if myfile:
            os.remove("./static/uploads/product/"+cover_pic)
    return render(request,"myadmin/info.html",context)