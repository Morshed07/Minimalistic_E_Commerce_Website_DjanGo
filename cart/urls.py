from django.urls import path
from .views import *
urlpatterns = [
    path('add-to-cart/<int:product_id>/',AddToCart.as_view(), name ='add-to-cart'),
    path('cart-details/',CartView.as_view(), name = 'cart-details'),
    path('add-coupon/',AddCoupon.as_view(), name = 'add-coupon')
]
