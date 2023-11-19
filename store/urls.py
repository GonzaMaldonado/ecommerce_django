from django.urls import path
from .views import (Home, DetailProduct, MyOrders, Cart, Checkout, create_checkout_session,
                    stripe_webhook, update_item, SuccessView, CancelledView)

urlpatterns = [
  path('', Home.as_view(), name="home"),
  path('detail/<str:id>/', DetailProduct.as_view(), name="product_detail"),
  path('my_orders/', MyOrders.as_view(), name="my_orders"),
  path('cart/', Cart.as_view(), name="cart_page"),
  path('checkout/', Checkout.as_view(), name="checkout"),
  path('create-checkout-session/', create_checkout_session),
  path('webhook/', stripe_webhook),
  path('success/', SuccessView.as_view()),
  path('cancelled/', CancelledView.as_view()),
  path('update_item/', update_item, name="update_item"),
]