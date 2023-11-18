import json
import stripe
from .models import CartItem

def cart_context(request):
  if request.user.is_authenticated:
    cart = CartItem.objects.filter(user=request.user)
    total = sum([item.get_total for item in cart])
    quantity = sum([item.quantity for item in cart])
    is_digital = [item.digital for item in cart]
    shipping = False in is_digital
    return {'cart': cart, 'total': total, 'quantity': quantity, 'shipping': shipping}
  else:
    try:
      cart_cookie = json.loads(request.COOKIES['cart'])
      total = 0
      quantity = 0
      shipping = False
      cart = []

      for product_id in cart_cookie:
        product = stripe.Product.retrieve(product_id)
        amount = stripe.Price.list(product=product.id)
        price = amount.data[0].unit_amount / 100
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

    return {'cart': cart, 'total': total, 'quantity': quantity, 'shipping': shipping}