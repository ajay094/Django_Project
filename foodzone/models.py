from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
	productname = models.CharField(max_length=100)
	product_image= models.ImageField(upload_to='product_image/',default='brand.png',null=True,blank=True)
	price = models.PositiveIntegerField()
	description = models.CharField(max_length=40)

class Orders(models.Model):
	STATUS = [('Pending','Pending'),('Order Confirmed','Order Confirmed'),('Out for Delivery','Out for Delivery'),('Delivered','Delivered')]
	product = models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
	email = models.CharField(max_length=50,null=True)
	address = models.CharField(max_length=300,null=False)
	mobile = models.CharField(max_length=10)
	status = models.CharField(max_length = 50,null = True,choices=STATUS)