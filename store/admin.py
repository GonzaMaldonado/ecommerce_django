from django.contrib import admin
from .models import Order, CartItem, ShippingAddress

admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(ShippingAddress)