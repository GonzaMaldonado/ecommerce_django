from django.urls import path
from .views import (Home, DetailProduct, Cart, Checkout, stripe_config, create_checkout_session,
                    update_item, process_order, SuccessView, CancelledView)

urlpatterns = [
  path('', Home.as_view(), name="home"),
  path('<str:id>/', DetailProduct.as_view(), name="product_detail"),
  path('cart/', Cart.as_view(), name="cart"),
  path('checkout/', Checkout.as_view(), name="checkout"),
  path('config/', stripe_config, name="config"),
  path('create-checkout-session/', create_checkout_session, name="create_checkout"),
  path('success/', SuccessView.as_view()),
  path('cancelled/', CancelledView.as_view()),
  path('update_item/', update_item, name="update_item"),
  path('process_order/', process_order, name="process_order"),
]