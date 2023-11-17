from django.contrib import admin
from .models import Category, Order, CartItem, ShippingAddress

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(ShippingAddress)