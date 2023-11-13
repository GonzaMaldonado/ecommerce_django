import json
from .models import Product, Order

def cookieCart(request):
  try:
      cart = json.loads(request.COOKIES['cart'])
  except:
      cart= {}

  items = []
  order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

  for i in cart:
    try:
        product = Product.objects.get(id=i)
        total = product.price * cart[i]['quantity']
        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']
        item = {
          'product': {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'imageURL': product.imageURL
          },
          'quantity': cart[i]['quantity'],
          'get_total': total
        }
        items.append(item)

        if product.digital == False:
          order['shipping'] = True
    except:
        pass

  return {'items': items, 'order': order}


def cartData(request):
  if request.user.is_authenticated:
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    items = order.orderitems.all()
  else:
    cookieData = cookieCart(request)
    items = cookieData['items']
    order = cookieData['order']
    
  return {'order': order, 'items': items}