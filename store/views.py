import json
import stripe
from django.views.generic import TemplateView
from .models import Order, OrderItem, Category, ShippingAddress
from .utils import cartData, cookieCart

from django.conf import settings
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


class Home(TemplateView): 
  template_name = "store/store.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    products = stripe.Product.list()
    prices = stripe.Price.list()

    for product ,price in zip(products, prices):
       product['price'] = price.unit_amount / 100

    data = cartData(self.request)
    context['get_cart_items'] = data['get_cart_items']
    context['products'] = products
    context['prices'] = prices
    return context


class Cart(TemplateView):
  template_name = "store/cart.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    data = cartData(self.request)
    context['items'] = data['items']
    context['get_cart_items'] = data['get_cart_items']
    context['get_cart_total'] = data['get_cart_total']
    return context


class Checkout(TemplateView):
  template_name = "store/checkout.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    data = cartData(self.request)
    context['items'] = data['items']
    context['get_cart_items'] = data['get_cart_items']
    context['get_cart_total'] = data['get_cart_total']
    context['shipping'] = data['shipping']
    return context


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create
            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            if request.user.is_authenticated:
              items = cartData(request)
              cart_items = items['items']
            else:
              items = cookieCart(request)
              cart_items = items['items']
               
            line_items = []
            for item in cart_items:
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item['product']['price'] * 100),  # El precio debe estar en centavos
                        'product_data': {
                            'name': item['product']['name'],
                        }
                    },
                    'quantity': item['quantity']
                })


            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items
            )
            total = checkout_session['amount_total'] / 100
            if request.user.is_authenticated:
              order = Order.objects.create(id=checkout_session['id'] ,user=request.user, total=total)
              order.save()
              OrderItem.objects.filter(user=request.user).delete()
            else:
              Order.objects.create(id=checkout_session['id'], total=total)
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


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

  orderItem, created = OrderItem.objects.get_or_create(
     user=request.user,
     product=productId,
     price=price,
     digital=product.metadata.digital
  )

  if action == 'add':
    orderItem.quantity += 1
  elif action == 'remove':
    orderItem.quantity -= 1

  orderItem.save()

  if orderItem.quantity <= 0:
    orderItem.delete()
  return JsonResponse('Item was added', safe=False)


def process_order(request):
  pass
  """ 
  return JsonResponse('Payment complete', safe=False) """
  
class SuccessView(TemplateView):
    template_name = 'store/success.html'


class CancelledView(TemplateView):
    template_name = 'store/cancelled.html'