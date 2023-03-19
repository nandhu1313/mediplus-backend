from django.contrib import admin
from home.models import Product, User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','name','phone','email','location','password']
    list_editable = ['name','phone','email','location','password']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','mrp','orp','category','description','image']
    list_editable = ['title','mrp','orp','category','description','image']