from django.urls import path
from .views import home,  cart, checkout, update_item, process_order

urlpatterns = [
  path('', home, name="home"),
  path('cart/', cart, name="cart"),
  path('checkout/', checkout, name="checkout"),
  path('update_item/', update_item, name="update_item"),
  path('process_order/', process_order, name="process_order"),
]