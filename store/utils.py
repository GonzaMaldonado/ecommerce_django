import json
import stripe
from .models import Order, CartItem


def cookieCart(request):
  items = []
  get_cart_items = 0
  get_cart_total = 0
  shipping = False

  try:
      cart = json.loads(request.COOKIES['cart'])
  except:
      cart= {}

  for product_id in cart:
    try:
        product = stripe.Product.retrieve(product_id)
        amount = stripe.Price.list(product=product.id)
        price = amount.data[0].unit_amount / 100
        total = price * cart[product_id]['quantity']
        get_cart_total += total
        get_cart_items += cart[product_id]['quantity']
        item = {
          'product': {
            'id': product.id,
            'name': product.name,
            'price': price,
            'images': product.images
          },
          'quantity': cart[product_id]['quantity'],
          'get_total': total,
        }

        items.append(item)
        if product.metadata.digital == 'False':
          shipping = True       
    except:
        pass

  return {'items': items, 'shipping': shipping, 'get_cart_items': get_cart_items, 'get_cart_total': get_cart_total}


def cartData(request):
  get_cart_items= 0
  get_cart_total= 0
  shipping = False
  orders = CartItem.objects.filter(user=request.user)

  items = []
  for order in orders:
    try:
      product = stripe.Product.retrieve(order.product)
      price = order.price
      total = price * order.quantity
      get_cart_total += total
      get_cart_items += order.quantity
      item = {
        'product': {
          'id': product.id,
          'name': product.name,
          'price': price,
          'images': product.images
        },
        'quantity': order.quantity,
        'get_total': total,
      }

      items.append(item)
      if order.digital == False:
        shipping = True    
    except:
      pass
    
  return {'items': items, 'get_cart_items': get_cart_items, 'get_cart_total': get_cart_total, 'shipping': shipping}

# Cuando un usuario hace un pedido y no esta autenticado
""" def guestOrder(request, data):
    #name = data['form']['name']
    #username = f'{name}_{randint(0, 10000)}'
    #email = data['form']['email']

    cookieData = cookieCart(request)
    print(cookieData)

    #user, created = User.objects.get_or_create(
     # username=username,
      #email=email
    #)
    #user.save()

    return items, user """