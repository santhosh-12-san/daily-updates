from django.contrib import admin
from .models import Category, Product
from .models import Category, Product, Slider

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'in_stock', 'category']
    list_editable = ['price', 'in_stock']
    
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
   list_display = ['title', 'image']