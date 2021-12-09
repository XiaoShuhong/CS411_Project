from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
# Create your views here.
from myadmin.models import User
from django.db import connection

def index(request,pIndex=1):
    ulist=[]
    with connection.cursor() as cursor:
        insert_stmt1=(
                "select * from staff where status !=9"
                )
        cursor.execute(insert_stmt1)
        rows_all=cursor.fetchall()
        for row in rows_all:
                u_dict={}
                u_dict['id']=row[0]
                u_dict['username']=row[1]
                u_dict['nickname']=row[2]
                u_dict['password_hash']=row[3]
                u_dict['password_salt']=row[4]
                u_dict['status']=row[5]
                u_dict['create_at']=row[6]
                u_dict['update_at']=row[7]
                insert_stmt2=(
                "select user_id from salary "
                )
                cursor.execute(insert_stmt2)
                staff_id_all=cursor.fetchall()
                id_list=[]
                for staff_id in staff_id_all:
                    if staff_id[0] not in id_list:
                        id_list.append(staff_id[0])
                # print(id_list)
                if u_dict['id'] in id_list:
                    insert_stmt3=(
                        "SELECT sum(salary.money) FROM salary join staff on salary.user_id = staff.id  where salary.user_id = %s group by salary.user_id"
                    )
                    data=[u_dict['id']]
                    cursor.execute(insert_stmt3,data)
                    salary_output=cursor.fetchone()
                    # print(salary_output[0])
                    u_dict['salary']=salary_output[0]

                else:
                    u_dict['salary']=0



                ulist.append(u_dict)

        
                # print(kw_dict)
    # umod = User.objects
    # ulist = umod.filter(status__lt=9)

    mywhere=[]
    # print(ulist)
    # print(type(ulist))
    kw = request.GET.get("keyword",None)
    if kw:
        # ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append('keyword='+kw)
        with connection.cursor() as cursor:
            var1 = '%' + kw + '%'
            insert_stmt=(
            "select * from staff where username like %s or nickname like %s and status !=9"
            )
            data=(var1,var1)
            cursor.execute(insert_stmt,data)
            rows=cursor.fetchall()
            kwlist=[]
            for row in rows:
                kw_dict={}
                kw_dict['id']=row[0]
                kw_dict['username']=row[1]
                kw_dict['nickname']=row[2]
                kw_dict['password_hash']=row[3]
                kw_dict['password_salt']=row[4]
                kw_dict['status']=row[5]
                kw_dict['create_at']=row[6]
                kw_dict['update_at']=row[7]
                insert_stmt4=(
                "select user_id from salary "
                )
                cursor.execute(insert_stmt4)
                kw_staff_id_all=cursor.fetchall()
                kw_id_list=[]
                for kw_staff_id in kw_staff_id_all:
                    if kw_staff_id[0] not in kw_id_list:
                        kw_id_list.append(kw_staff_id[0])
                if kw_dict['id'] in kw_id_list:
                    insert_stmt5=(
                        "SELECT sum(salary.money) FROM salary join staff on salary.user_id = staff.id  where salary.user_id = %s group by salary.user_id"
                    )
                    data=[kw_dict['id']]
                    cursor.execute(insert_stmt5,data)
                    salary_output=cursor.fetchone()
                    # print(salary_output[0])
                    kw_dict['salary']=salary_output[0]

                else:
                    kw_dict['salary']=0
                kwlist.append(kw_dict)
                # print(kw_dict)
                
                # kwlist.append(row)
        cursor.close()
                

        
        # for p in User.objects.raw('SELECT * FROM staff where username ='+str(kw)):
        #     print(p)
     
    # status = request.GET.get('status','')
    # if status != '':
    #     ulist = ulist.filter(status=status)
    #     mywhere.append("status="+status)

    
    if kw:
        pIndex = int(pIndex)
        page = Paginator(kwlist,5) 
        maxpages = page.num_pages 
    else:
        pIndex = int(pIndex)
        page = Paginator(ulist,5) 
        maxpages = page.num_pages 
   
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) 
    plist = page.page_range 
    context = {"userlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/user/index.html",context)

def add(request):
    
    return render(request,"myadmin/user/add.html")

def insert(request):
    
    try:
        # ob = User()
        # ob.username = request.POST['username']
        # ob.nickname = request.POST['nickname']
   
        # import hashlib,random
        # md5 = hashlib.md5()
        # n = random.randint(100000, 999999)
        # s = request.POST['password']+str(n) 
        # md5.update(s.encode('utf-8'))
        # ob.password_hash = md5.hexdigest() 
        # ob.password_salt = n
        # ob.status = 1
        # ob.create_at = datetime.now().strftime("%Y-%m-%d")
        # ob.update_at = datetime.now().strftime("%Y-%m-%d")
        # ob.save()
        # context = {'info':"Insert Success"}
        username=request.POST['username']
        nickname=request.POST['nickname']
        import hashlib,random
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password']+str(n) 
        md5.update(s.encode('utf-8'))
        password_hash = md5.hexdigest() 
        password_salt = n
        status = 1
        create_at = datetime.now().strftime("%Y-%m-%d")
        update_at = datetime.now().strftime("%Y-%m-%d")
        insert_stmt=(
            "insert into staff(username,nickname,password_hash,password_salt,status,create_at,update_at)"
            "values (%s,%s,%s,%s,1,%s,%s)"
        )
        data=(username,nickname,password_hash,password_salt,create_at,update_at)
        with connection.cursor() as cursor:
            cursor.execute(insert_stmt,data)
        context = {'info':"Insert Success"}
    except Exception as err:
        print(err)
        context = {'info':"Insert Fail"}
    return render(request,"myadmin/info.html",context)

def delete(request,uid=0):

    try:
        insert_stmt=(
            "delete from staff where id="+str(uid)
        )
        with connection.cursor() as cursor:
            cursor.execute(insert_stmt)
        # ob = User.objects.get(id=uid)
        # ob.status = 9
        # ob.update_at = datetime.now().strftime("%Y-%m-%d")
        # ob.save()
        context = {'info':"Delete Success"}

    except Exception as err:
        print(err)
        context = {'info':"Delete Fail"}
    return render(request,"myadmin/info.html",context)

def edit(request,uid=0):
 
    try:
        ob = User.objects.get(id=uid)
        context = {'user':ob}
        return render(request,"myadmin/user/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':"Edit Error"}
        return render(request,"myadmin/info.html",context)

def update(request,uid):
  
    try:
        nickname = request.POST['nickname']
        status = request.POST['status']
        update_at = datetime.now().strftime("%Y-%m-%d")
        insert_stmt=(
            "update staff set nickname=%s,status=%s,update_at=%s where id=%s"
        )
        data=(nickname,status,update_at,uid)
        with connection.cursor() as cursor:
            cursor.execute(insert_stmt,data)
        
        # ob = User.objects.get(id=uid)
        # ob.nickname = request.POST['nickname']
        # ob.status = request.POST['status']
        # ob.update_at = datetime.now().strftime("%Y-%m-%d")
        # ob.save()
        context = {'info':"Update Success"}
    except Exception as err:
        print(err)
        context = {'info':"Update Fail"}
    return render(request,"myadmin/info.html",context)