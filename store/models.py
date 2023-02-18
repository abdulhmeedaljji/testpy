from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.contrib.auth.models import User
from colorfield.fields import ColorField

# Create your models here.




class Mobiles(models.Model):
  placeToUpload = 'Mobiles'
  image = models.ImageField(upload_to=placeToUpload, null=True)
  screan = models.CharField(max_length=250)
  mobile_color = ColorField(default='#FF0000')
  mobile_color2 = ColorField(default='#FC0000')
  mobile_color3 = ColorField(default='#FB0000')
  mobile_color4 = ColorField(default='#FA0000')
  coverage = models.CharField(max_length=250)
  camera=models.CharField(max_length=250)
  core=models.CharField(max_length=250)
  battery=models.CharField(max_length=250)
  front=models.CharField(max_length=250)
  name=models.CharField(max_length=250, default=False)

  def __str__(self):
    return self.name


class Category(models.Model):
  name = models.CharField(max_length=250)
  def __str__(self):
    return self.name

class Products(models.Model):
  name = models.CharField(max_length=250)
  size=models.FloatField(default=None)
  color=models.CharField(max_length=250,default=None)
  description = models.TextField()
  price = models.FloatField()
  placeToUpload = 'products'
  image = models.ImageField(upload_to=placeToUpload, null=True)
  Cat=models.ForeignKey(Category ,on_delete=models.CASCADE)

  screan = models.CharField(max_length=250)
  mobile_color = ColorField(default='#FF0000')
  mobile_color2 = ColorField(default='#FC0000')
  mobile_color3 = ColorField(default='#FB0000')
  mobile_color4 = ColorField(default='#FA0000')
  coverage = models.CharField(max_length=250)
  camera = models.CharField(max_length=250)
  core = models.CharField(max_length=250)
  battery = models.CharField(max_length=250)
  front = models.CharField(max_length=250)

  def __str__(self):
    return self.name



class ProductsImages(models.Model):
  Covergimage = models.ImageField(upload_to='placeToUpload', null=True)
  Battrayimage = models.ImageField(upload_to='placeToUpload', null=True)
  Coreimage = models.ImageField(upload_to='placeToUpload', null=True)
  Frontimage = models.ImageField(upload_to='placeToUpload', null=True)
  Cameraimage = models.ImageField(upload_to='placeToUpload', null=True)
  ProductImage=models.ForeignKey(Products ,on_delete=models.CASCADE,blank=True,null=True)





# class Category(models.Model):
#   name = models.CharField(max_length=250)
#   def __str__(self):
#     return self.name

class Product(models.Model):
  name = models.CharField(max_length=250)
  description = models.TextField()
  color=models.CharField(max_length=250)
  size=models.FloatField()
  price = models.FloatField()
  placeToUpload = 'products'
  image = models.ImageField(upload_to=placeToUpload, null=True)
  def __str__(self):
    return self.name

  # @property
  # def get_products(self):
  #    return Product.objects.filter(categories__name=self.category)

  @property
  def image_url(self):
    try:
      url = self.image.url
    except:
      url=""
    return url



class Order(models.Model):
  customer=models.ForeignKey(User ,on_delete=models.SET_NULL,blank=True,null=True )
  data_orderd=models.DateTimeField(auto_now_add=True)
  complete=models.BooleanField(default=False,null=True,blank=False)
  transaction_id=models.CharField(max_length=300,null=True)

  def str(self):
      return str(self.id)

  @property
  def get_cart_total(self):
    orderitems = OrderItem.objects.filter(order = self.id)
    total = sum([item.get_total for item in orderitems])
    return total

  @property
  def get_cart_items(self):
    orderitems = OrderItem.objects.filter(order = self.id)
    total= sum([item.quantity for item in orderitems])
    return total

class OrderItem(models.Model):
  product =models.ForeignKey(Product ,on_delete=models.SET_NULL,blank=True,null=True )
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
  quantity=models.IntegerField(default=0,null=True,blank=True)
  data_added = models.DateTimeField(auto_now_add=True)

  @property
  def get_total(self):
      total=self.product.price * self.quantity
      return  total

