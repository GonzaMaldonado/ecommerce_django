import json
import stripe
from django.conf import settings
from .models import CartItem

def cart_context(request):
  cart = []
  total = 0
  quantity = 0
  shipping = False

  if request.user.is_authenticated:
    cart_items = CartItem.objects.filter(user=request.user)
    for cart_item in cart_items:        
        item = {
          'id': cart_item.id,
          'name': cart_item.name,
          'price': cart_item.price,
          'image': cart_item.image,
          'quantity': cart_item.quantity,
          'get_total': cart_item.get_total
        }
        cart.append(item)

        total += cart_item.get_total
        quantity += cart_item.quantity

        if cart_item.digital == False:
          shipping = True   
  else:
    try:
      cart_cookie = json.loads(request.COOKIES['cart'])
      stripe.api_key = settings.STRIPE_SECRET_KEY

      for product_id in cart_cookie:
        product = stripe.Product.retrieve(product_id)
        price = float(cart_cookie[product_id]['price'])
        get_total = price * cart_cookie[product_id]['quantity']
        
        item = {
          'id': product.id,
          'name': product.name,
          'price': price,
          'image': product.images[0],
          'quantity': cart_cookie[product_id]['quantity'],
          'get_total': get_total
        }
        cart.append(item)

        total += get_total
        quantity += cart_cookie[product_id]['quantity']

        if product.metadata.digital == 'False':
          shipping = True       
    except:
      cart = {}
      print('Cart not found')
  return {'cart': cart, 'total': total, 'quantity': quantity, 'shipping': shipping}
  