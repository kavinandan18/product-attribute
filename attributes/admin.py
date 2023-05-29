from django.contrib import admin
from .models import Family, Category, Brand, Product, ProductAttribute

admin.site.register(Family)
admin.site.register(Category)
admin.site.register(Brand)

class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeInline]
