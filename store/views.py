import json
import stripe
from django.views.generic import TemplateView
from .models import Order, CartItem, ShippingAddress

from django.conf import settings
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect


class Home(TemplateView): 
  template_name = "store/store.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    products = stripe.Product.list()
    prices = stripe.Price.list()

    for product ,price in zip(products, prices):
       product['price'] = price.unit_amount / 100

    context['products'] = products
    return context


class DetailProduct(TemplateView):
  template_name = 'store/detail_product.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    product = stripe.Product.retrieve(self.kwargs['id'])
    price = stripe.Price.list(product=product.id)

    context['product'] = product
    context['price'] = price.data[0].unit_amount / 100
    return context


class MyOrders(TemplateView):
   template_name = 'store/my_orders.html'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      orders = Order.objects.filter(user=self.request.user)
      context['orders'] = orders
      return context


class Cart(TemplateView):
  template_name = "store/cart.html"


class Checkout(TemplateView):
  template_name = 'store/checkout.html'
  

class SuccessView(TemplateView):
    template_name = 'store/success.html'


class CancelledView(TemplateView):
    template_name = 'store/cancelled.html'


@csrf_exempt
def create_checkout_session(request):
  if request.method == 'GET':
    domain_url = 'http://localhost:8000/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    line_items = []
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user=request.user)
      for item in cart_items:
          line_items.append({
            'price_data': {
              'currency': 'usd',
              'unit_amount': int(item.price) * 100,  # El precio debe estar en centavos
              'product_data': {
                'name': item.name,
              }
            },
            'quantity': item.quantity
          })
    else:
        try:
          cart_items = json.loads(request.COOKIES['cart'])
        except:
          cart_items = {}
        for productId in cart_items:
          product = stripe.Product.retrieve(productId)
          price = float(cart_items[productId]['price']) * 100
          line_items.append({
            'price_data': {
              'currency': 'usd',
              'unit_amount': int(price),  # El precio debe estar en centavos
              'product_data': {
                'name': product.name,
              }
            },
            'quantity': cart_items[productId]['quantity']
          })

    try:
      
      checkout_session = stripe.checkout.Session.create(
        success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=domain_url + 'cancelled/',
        payment_method_types=['card'],
        mode='payment',
        line_items=line_items,
        shipping_address_collection={'allowed_countries': ['AR']},
      )
      print("Checkout Session \n", checkout_session)
      total = checkout_session['amount_total'] / 100
      if request.user.is_authenticated:
        order = Order.objects.create(id=checkout_session['id'], user=request.user, total=total)
        order.save()
        CartItem.objects.filter(user=request.user).delete()
      else:
        order = Order.objects.create(id=checkout_session['id'], total=total)
        order.save()
    except Exception as e:
      return JsonResponse({'error': str(e)})
    return redirect(checkout_session.url, code=303)


@csrf_exempt # Para confirmar el pago en su totalidad
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        print(event)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)


# Para usuarios autenticados
def update_item(request):
  data = json.loads(request.body)
  action = data['action']
  productId = data['productId']
  product = stripe.Product.retrieve(productId)
  amount = stripe.Price.list(product=product.id)
  price = amount.data[0].unit_amount / 100

  cartItem, created = CartItem.objects.get_or_create(
     user=request.user,
     id=productId,
     name=product.name,
     image=product.images[0],
     price=price,
     digital=product.metadata.digital
  )

  if action == 'add':
    cartItem.quantity += 1
  elif action == 'remove':
    cartItem.quantity -= 1

  cartItem.save()

  if cartItem.quantity <= 0:
    cartItem.delete()
  return JsonResponse('Item was added', safe=False)
