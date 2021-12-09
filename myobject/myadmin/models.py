from django.db import models
from datetime import datetime


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50)   
    nickname = models.CharField(max_length=50)    
    password_hash = models.CharField(max_length=100)
    password_salt = models.CharField(max_length=50)    
    status = models.IntegerField(default=1)    
    create_at = models.DateTimeField(default=datetime.now)   
    update_at = models.DateTimeField(default=datetime.now)    

    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'password_hash':self.password_hash,'password_salt':self.password_salt,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d'),'update_at':self.update_at.strftime('%Y-%m-%d')}

    class Meta:
        db_table = "staff"  
        
class Shop(models.Model):
    name = models.CharField(max_length=255)        
    cover_pic = models.CharField(max_length=255)
    banner_pic = models.CharField(max_length=255)
    address = models.CharField(max_length=255)    
    phone = models.CharField(max_length=255)    
    status = models.IntegerField(default=1)        
    create_at = models.DateTimeField(default=datetime.now)    
    update_at = models.DateTimeField(default=datetime.now)   

    def toDict(self):
        
        return {'id':self.id,'name':self.name,'cover_pic':self.cover_pic,'banner_pic':self.banner_pic,'address':self.address,'phone':self.phone,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d'),'update_at':self.update_at.strftime('%Y-%m-%d')}

    class Meta:
        db_table = "shop" 




class Category(models.Model):
    shop_id = models.IntegerField()       
    name = models.CharField(max_length=50)
    status = models.IntegerField(default=1)        
    create_at = models.DateTimeField(default=datetime.now)    
    update_at = models.DateTimeField(default=datetime.now)    

    class Meta:
        db_table = "category"  

class Product(models.Model):
    shop_id = models.IntegerField()        
    category_id = models.IntegerField()   
    cover_pic = models.CharField(max_length=50)   
    name = models.CharField(max_length=300)
    price = models.FloatField()    
    status = models.IntegerField(default=1)        
    create_at = models.DateTimeField(default=datetime.now)    
    update_at = models.DateTimeField(default=datetime.now)   

    def toDict(self):
        return {'id':self.id,'shop_id':self.shop_id,'category_id':self.category_id,'cover_pic':self.cover_pic,'name':self.name,'price':self.price,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d'),'update_at':self.update_at.strftime('%Y-%m-%d')}

    class Meta:
        db_table = "product"  


class Member(models.Model):
    nickname = models.CharField(max_length=50)    
    avatar = models.CharField(max_length=255)   
    mobile = models.CharField(max_length=50)    
    status = models.IntegerField(default=1)        
    create_at = models.DateTimeField(default=datetime.now)    
    update_at = models.DateTimeField(default=datetime.now)   

    def toDict(self):
        return {'id':self.id,'nickname':self.nickname,'avatar':self.avatar,'mobile':self.mobile,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d'),'update_at':self.update_at.strftime('%Y-%m-%d')}

    class Meta:
        db_table = "vip"  