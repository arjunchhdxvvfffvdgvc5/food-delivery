from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class userType(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    type=models.CharField(max_length=100,null=True)

class Customersignup(models.Model):
      user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
      mobile=models.CharField(max_length=100,null=True)
      address=models.CharField(max_length=100,null=True)

class restaurentsignup(models.Model):
      user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
      mobile=models.CharField(max_length=100,null=True)
      address=models.CharField(max_length=100,null=True)
      image=models.FileField(null=True)

class agentsignup(models.Model):
      user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
      mobile=models.CharField(max_length=100,null=True)
      address=models.CharField(max_length=100,null=True)
      status=models.CharField(max_length=100,null=True,default="available")

class addmenu(models.Model):
    user=models.ForeignKey(restaurentsignup,on_delete=models.CASCADE,null=True)
    FoodName=models.CharField(max_length=100,null=True)
    description=models.CharField(max_length=100,null=True)
    price=models.IntegerField(null=True)
    quantity=models.IntegerField(null=True)
    image=models.FileField(null=True)

class product_cart(models.Model):
    product = models.ForeignKey(addmenu, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Customersignup, on_delete=models.CASCADE,null=True)
    quantity = models.CharField(max_length=50,null=True)
    status=models.CharField(max_length=50,null=True)
    total = models.CharField(max_length=100,null=True)


class assigned_order(models.Model):
      agent = models.ForeignKey(agentsignup, on_delete=models.CASCADE,null=True)
      user=models.ForeignKey(product_cart, on_delete=models.CASCADE,null=True)
      price=models.CharField(max_length=50)
      quantity=models.CharField(max_length=50)
      status=models.CharField(max_length=50)
      
class feedback(models.Model):
    user=models.ForeignKey(Customersignup,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=100,null=True)
    description=models.CharField(max_length=200,null=True)
    rating=models.CharField(max_length=200,null=True)
     

class agentWorks(models.Model):
    user=models.ForeignKey(agentsignup,on_delete=models.CASCADE,null=True)
    work=models.ForeignKey(assigned_order,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=200,null=True)
