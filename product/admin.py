from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'category', 'price', 'stock', 'slug']
#     prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product)    
admin.site.register(Cart)    
admin.site.register(CartItem)    