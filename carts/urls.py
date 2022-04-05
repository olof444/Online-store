from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('increase/<int:cart_item_id>', views.increase, name='increase'),
    path('remove_cart/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout')
]