from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.
from myadmin.models import User,Shop,Category,Product

def index(request):
    
    return redirect(reverse("web_index"))

def webindex(request):
    
    cartlist = request.session.get('cartlist',{})
    total_money = 0 
  
    for vo in cartlist.values():
        total_money += vo['total_money']
    request.session['total_money'] = total_money 
    
   
    context = {'categorylist':request.session.get("categorylist",{}).items()}
    return render(request,"web/index.html",context)

def login(request):

    shoplist = Shop.objects.filter(status=1)
    context = {'shoplist':shoplist}
    return render(request, "web/login.html",context)

def dologin(request):
    try:
   
        if request.POST['shop_id'] == '0':
            return redirect(reverse('web_login')+"?errinfo=1")

       
        user = User.objects.get(username=request.POST['username'])
        
        if user.status == 6 or user.status == 1:
           
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['pass']+user.password_salt 
            md5.update(s.encode('utf-8')) 
            if user.password_hash == md5.hexdigest(): 
                print('Login Success')
                
                request.session['webuser'] = user.toDict()
        
                shopob = Shop.objects.get(id=request.POST['shop_id'])
                request.session['shopinfo'] = shopob.toDict()
                
                clist = Category.objects.filter(shop_id = shopob.id,status=1)
                categorylist = dict() 
                productlist = dict() 
              
                already_list=[]
                for vo in clist:
                    id=(vo.name.split(" ")[2])
                    if id not in already_list:
                        already_list.append(id)

                        c = {'id':vo.id,'name':vo.name,'pids':[]}
                    
                        plist = Product.objects.filter(shop_id = shopob.id,category_id=id,status=1)
                  
                    
                        for p in plist:
                            c['pids'].append(p.toDict())
                            productlist[p.id]=p.toDict()
                        categorylist[vo.id] = c   
             
                request.session['categorylist'] = categorylist
                request.session['productlist'] = productlist
                
              
                return redirect(reverse("web_index"))
            else:
                return redirect(reverse('web_login')+"?errinfo=4")
        else:
            return redirect(reverse('web_login')+"?errinfo=3")
    except Exception as err:
        print(err)
        return redirect(reverse('web_login')+"?errinfo=2")

def logout(request):
    
    del request.session['webuser']
    return redirect(reverse('web_login'))

