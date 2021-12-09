
from django.urls import path,include

from web.views import index,cart

urlpatterns = [
    path('', index.index, name="index"),

    path('login', index.login, name="web_login"), 
    path('dologin', index.dologin, name="web_dologin"), 
    path('logout', index.logout, name="web_logout"), 
   


    path("web/",include([
        path('', index.webindex, name="web_index"), 

        path('cart/add/<str:pid>', cart.add, name="web_cart_add"),
        path('cart/delete/<str:pid>', cart.delete, name="web_cart_delete"), 
        path('cart/clear', cart.clear, name="web_cart_clear"), 
        path('cart/change', cart.change, name="web_cart_change"), 
        path('cart/pay', cart.pay, name="web_cart_pay"), 
        path('cart/check_discount', cart.check_discount, name="web_cart_discount"), 
    ]))


]
