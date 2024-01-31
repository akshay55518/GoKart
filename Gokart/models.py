from django.db import models
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your models here.

class Banner(models.Model):
    title = models.CharField(max_length=100)
    banner_image=models.ImageField(upload_to='product/banner')
    def  __str__(self):
        return self.title

class Category(models.Model):
    id=models.CharField(primary_key=True,max_length=5)
    title=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to='product/Category')
    def __str__(self):
        return self.title
    
class Brand(models.Model):
    id=models.CharField(primary_key=True,max_length=10)
    brand_name=models.CharField(max_length=50)
    brand_logo=models.ImageField(upload_to='product/brand')
    def __str__(self):
        return self.brand_name
    
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField(default='')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    product_image=models.ImageField(upload_to='product/items')
    def __str__(self):
        return self.title
    
STATE_CHOICES=(
    ('Kerala','Kerala'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Jharkhand', 'Jharkhand'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ("Rajasthan", "Rajasthan"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("Haryana", "Haryana"),
    ("Delhi", "Delhi"),
    ("West Bengal","West Bengal")
)
    
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=100)
    def  __str__(self):
        return self.name
    
    
    
    
    
