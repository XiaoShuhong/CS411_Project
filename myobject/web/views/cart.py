from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.db import connection
from myadmin.models import User


def add(request,pid):
   
    product = request.session['productlist'][pid]
    product['num'] = 1 

    # p_id=product['id']
    # s_id=product['shop_id']
    # name=product['name']
    # status=product['status']
    # num=product['num']
    # price=product['price']
    # print(product['shop_id'])
    # print(product['name'])
    # print(product['num'])
    # print(product['status'])
    # print(product.keys())
    cartlist = request.session.get('cartlist',{})
    
    if pid in cartlist:
        cartlist[pid]['num'] += product['num']
            # stmt1=(
            #     "select quantity from order_detail where product_id=%s and shop_id=%s "
            # )
            # data1=(p_id,s_id)
            # cursor.execute(stmt1,data1)
            # old_num=cursor.fetchone()[0]
            # new_num=old_num+1
            # # print(old_num,type(old_num))
            # stmt2=("update order_detail set quantity =%s where product_id=%s and shop_id=%s ")
            # data2=(new_num,p_id,s_id)
            # cursor.execute(stmt2,data2)

    else:
        cartlist[pid] = product 
            # stmt3=(
            #     "insert into order_detail (shop_id,product_id,product_name,price,quantity,status) values (%s,%s,%s,%s,%s,%s)"
            # )
            # data3=(s_id,p_id,name,price,num,status)
            # cursor.execute(stmt3,data3)
    
    
    # print(cartlist)
    
    cartlist[pid]["total_money"]=cartlist[pid]['num']*cartlist[pid]['price']
        
    request.session['cartlist'] = cartlist
    # print(cartlist)
   
    return redirect(reverse('web_index'))

def delete(request,pid):

    
    cartlist = request.session.get('cartlist',{})
    del cartlist[pid]
    
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))

def clear(request):

    request.session['cartlist'] = {}
    return redirect(reverse('web_index'))


def change(request):

    
    cartlist = request.session.get('cartlist',{})
    pid = request.GET.get("pid",0) 
    m = int(request.GET.get('num',1)) 
    if m < 1:
        m = 1
    cartlist[pid]['num'] = m 

    cartlist[pid]["total_money"]=cartlist[pid]['num']*cartlist[pid]['price']
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))


def pay(request):
    cartlist=request.session.get('cartlist',{})
    p_id=[]
    s_id=[]
    name=[]
    status=[]
    num=[]
    price=[]
    user = request.session.get('webuser',{})
    
    u_id=user['username']

    for pid in cartlist:
        # print(pid)
        p_id.append(pid)
        s_id.append(cartlist[pid]['shop_id'])
        name.append(cartlist[pid]['name'])
        status.append(cartlist[pid]['status'])
        num.append(cartlist[pid]['num'])
        price.append(cartlist[pid]['price'])
        # tot_price.append(cartlist[pid]['total_money'])
        # print(type(pid))
   
    with connection.cursor() as cursor:
        stmt3=(
                    "delete from order_detail where id>0"
                )
                
        cursor.execute(stmt3)

        for i in range(len(p_id)):
            cur_pid=p_id[i]
            cur_sid=s_id[i]
            stmt2=(
                "select quantity, price from order_detail where product_id=%s and shop_id=%s"
            )
            data2=(cur_pid,cur_sid)
            cursor.execute(stmt2,data2)
            output=cursor.fetchone()
            if output==None:
                stmt1=(
                    "insert into order_detail (shop_id,product_id,product_name,price,quantity,status,user_id) values (%s,%s,%s,%s,%s,%s,%s)"
                )
                data1=(s_id[i],p_id[i],name[i],price[i],num[i],status[i],u_id)
                cursor.execute(stmt1,data1)
            
        stmt5=(
                "select * from order_detail"
            )
        cursor.execute(stmt5)
        all_output=cursor.fetchall()
        for opt in all_output:
            # print(opt)
            discount_price=opt[4]
            cur_num=opt[5]
            new_tot_price=discount_price*cur_num
            curpid=str(opt[2])
           
            # print(cartlist[curpid]['price'])
            # cartlist[curpid]['price']=discount_price
            cartlist[curpid]['total_money']=new_tot_price
        request.session['cartlist']=cartlist
        # print(cartlist)

    cursor.close()
    
    
    
    
    return redirect(reverse('web_index'))

def check_discount(request):

      
    with connection.cursor() as cursor:

        stmt7=(
                "select * from order_detail"
                )

        cursor.execute(stmt7)
        all_output1=cursor.fetchall()
        for opt in all_output1:
            # print(opt)
            vip_price=opt[4]
            cur_num=opt[5]
            cur_tot_price=vip_price*cur_num
            cur_pid=opt[2]
            cur_sid=opt[1]
            stmt8=(
                "update order_detail set total_price=%s where product_id=%s and shop_id=%s"
                )
            data8=(cur_tot_price,cur_pid,cur_sid)

            cursor.execute(stmt8,data8)


        procedure_name='Cnt_on_Cnt' 
        cursor.callproc(procedure_name,[])
        cartlist=request.session.get('cartlist',{})
        stmt6=(
                "select * from order_detail"
                )

        cursor.execute(stmt6)
        all_output=cursor.fetchall()
        for opt in all_output:
            # print(opt)
            tot_price=opt[7]
            curpid=str(opt[2])
           
            # print(cartlist[curpid]['price'])
            cartlist[curpid]['total_money']=tot_price
            request.session['cartlist']=cartlist

    return redirect(reverse('web_index'))
