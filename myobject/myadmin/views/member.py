from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.
from myadmin.models import Member

def index(request,pIndex=1):
    
    umod = Member.objects
    ulist = umod.filter(status__lt=9)
    mywhere=[]
    
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
    context = {"memberlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/member/index.html",context)

def delete(request,uid=0):
    
    try:
        ob = Member.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Delete Success"}
    except Exception as err:
        print(err)
        context = {'info':"Delete Error"}
    return render(request,"myadmin/info.html",context)
