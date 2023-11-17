import json
from .models import CartItem

def cart_context(request):
  if request.user.is_authenticated:
    cart = CartItem.objects.filter(user=request.user)
    return {'cart': cart}
  else:
    try:
      print('voy')

      cart = json.loads(request.COOKIES['cart'])
      print(cart)
    except:
      cart = {} 

      print("Cart: ", cart)
    return {'cart': cart}