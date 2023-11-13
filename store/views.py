import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Order, OrderItem, Category, ShippingAddress
from .utils import cartData

def home(request):
  products = Product.objects.all()
  categories = Category.objects.all()[:3]
  
  data = cartData(request)
  order = data['order']

  return render(request, 'store/store.html', {'products': products, 'order': order, 'categories': categories})


def cart(request):
  data = cartData(request)
  items = data['items']
  order = data['order']

  return render(request, 'store/cart.html', {'items': items, 'order': order})


def checkout(request):
  data = cartData(request)
  items = data['items']
  order = data['order']

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


def process_order(request):
  transaction_id = datetime.datetime.now().timestamp()
  data = json.loads(request.body)

  if request.user.is_authenticated:
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
      order.complete = True
    order.save()

    if order.shipping == True:
      ShippingAddress.objects.create(
        user=request.user,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode']
      )

  else:
    print('User is not login')

  return JsonResponse('Payment complete', safe=False)
  
