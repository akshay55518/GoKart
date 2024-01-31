from django.contrib import admin
from . models import Category,Product,Banner,Brand,Customer

# Register your models here.

@admin.register(Banner)
class BannerModelAdmin(admin.ModelAdmin):
    list_display = ('id','title','banner_image')
    
@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    list_display=('id','brand_name','brand_logo')

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','category_image']
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discount_price','category','quantity','product_image','description','composition']
    list_editable = ['description','composition']
    

    
@admin.register(Customer)
class  CustomerAddressModelAdmin(admin.ModelAdmin):
    list_display=['id','user','address','mobile','zipcode']