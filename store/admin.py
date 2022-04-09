from django.contrib import admin
from .models import Product, Variations, ReviewRating

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'created', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}


@admin.register(Variations)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'created', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'created', 'is_active')


admin.site.register(ReviewRating)