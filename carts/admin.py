from django.contrib import admin
from .models import Cart, Cart_item


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')


@admin.register(Cart_item)
class Cart_itemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')