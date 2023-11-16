from django.contrib import admin
from .models import Category, Order, OrderItem, ShippingAddress

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)