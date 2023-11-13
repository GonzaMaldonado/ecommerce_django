import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Order, OrderItem, Category

def home(request):
  products = Product.objects.all()
  categories = Category.objects.all()[:3]
  if request.user.is_authenticated:
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
  else:
    order = {'get_cart_total': 0, 'get_cart_items': 0}
  return render(request, 'store/store.html', {'products': products, 'order': order, 'categories': categories})


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
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
  return render(request, 'store/checkout.html', {'items': items, 'order': order})


def update_item(request):
  data = json.loads(request.body)
  productId = data['productId']
  action = data['action']
  product = Product.objects.get(id=productId)
  order, created = Order.objects.get_or_create(user=request.user, complete=False)

  orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

  if action == 'add':
    orderItem.quantity += 1
  elif action == 'remove':
    orderItem.quantity -= 1

  orderItem.save()

  if orderItem.quantity <= 0:
    orderItem.delete()
  return JsonResponse('Item was added', safe=False)