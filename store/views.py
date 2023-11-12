from django.shortcuts import render
from .models import Product, Order

def home(request):
  products = Product.objects.all()
  return render(request, 'store/store.html', {'products': products})


def cart(request):
  if request.user.is_authenticated:
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    items = order.orderitems.all()
  else:
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
  return render(request, 'store/cart.html', {'items': items, 'order': order})


def checkout(request):
  if request.user.is_authenticated:
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    items = order.orderitems.all()
  else:
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
  return render(request, 'store/checkout.html', {'items': items, 'order': order})