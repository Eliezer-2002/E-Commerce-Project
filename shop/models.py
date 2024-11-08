from django.db import models
from django.contrib.auth.models import User
import datetime
import os
from django.utils.text import slugify
import uuid

def getFileName(request,filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class SuperCategory(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    status = models.BooleanField(default=False,help_text="0-Show, 1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def display_status(self):
        return 'Hidden' if self.status else ''

    display_status.short_description = 'Status'

    def __str__(self):
        return f"{self.name} - {self.display_status()}"

class Category(models.Model):
    sup_category = models.ForeignKey(SuperCategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=False,blank=False)
    image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    description = models.CharField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-Show, 1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True,blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def display_status(self):
        return 'Hidden' if self.status else ''

    display_status.short_description = 'Status'

    def __str__(self):
        return f"{self.name} - {self.display_status()}"

class Products(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=False,blank=False)
    vendor = models.CharField(max_length=150,null=False,blank=False)
    product_image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    quantity = models.IntegerField(null=False,blank=False)
    original_price = models.FloatField(null=False,blank=False)
    selling_price = models.FloatField(null=False,blank=False)
    description = models.CharField(max_length=1500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-Show, 1-Hidden")
    trending = models.BooleanField(default=False,help_text="0-default, 1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200,unique=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or Products.objects.filter(slug=self.slug).exists():
            self.slug = f"{slugify(self.name)}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    #def save(self, *args, **kwargs):
    #    self.slug = slugify(self.name)
    #    super().save(*args, **kwargs)

    def display_status(self):
        return 'Hidden' if self.status else ''

    display_status.short_description = 'Status'

    def __str__(self):
        return f"{self.name} - {self.display_status()}"

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price

class Favourite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)      
    created_at = models.DateTimeField(auto_now_add=True)
    







    