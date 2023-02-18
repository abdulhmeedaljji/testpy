from django.contrib import admin
from store.models import Product,Category,Mobiles,Products,ProductsImages
# Register your models here.



admin.site.register(Mobiles)
admin.site.register(Products)
admin.site.register(Category)
admin.site.register(ProductsImages)

