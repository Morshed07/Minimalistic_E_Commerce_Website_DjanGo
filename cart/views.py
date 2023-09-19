from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from typing import Any
from django import http
from django.shortcuts import render
from django.shortcuts import get_object_or_404,redirect
from .carts import Cart
from product.models import Product
from .models import Coupon
from django.views.generic import View,TemplateView
# Create your views here.


class AddToCart(View):
    def post(self,*args, **kwargs):
        product = get_object_or_404(Product,id=kwargs.get('product_id'))
        cart = Cart(self.request)
        cart.update(product.id, 1)
        return redirect('product-details',slug=product.slug)
    
class CartView(TemplateView):
    template_name = 'cart/cart.html'

    def get(self, request, *args: Any, **kwargs: Any):

        product_id = request.GET.get('product_id',None)
        quantity = request.GET.get('quantity',None)
        clear = request.GET.get('clear',False)
        cart = Cart(request)
        
        if product_id and quantity:
            product = get_object_or_404(Product, id= product_id)
            if int(quantity) > 0:
                if product.in_stock:
                    cart.update(int(product_id),int(quantity))
                    return redirect ('cart-details')
                else:
                    messages.warning(request,"The product is not in stock anymore!")
                    return redirect('cart-details')
            else:
                cart.update(int(product_id),int(quantity))
                return redirect ('cart-details')
        if clear:
            cart.clear()
            return redirect ('cart-details')

        return super().get(request, *args, **kwargs)
    

class AddCoupon(View):
    def post(self, *args, **kwargs):
        code = self.request.POST.get('coupon', '')
        coupon = Coupon.objects.filter(code__iexact = code, active=True)
        cart = Cart(self.request)

        if coupon.exists():
            coupon = coupon.first()
            current_date = datetime.date(timezone.now())
            active_date = coupon.active_date
            expiry_date = coupon.expiry_date

            if current_date > expiry_date:
                messages.warning(self.request,"The coupon has been expired!")
                return redirect('cart-details')
            
            if current_date < active_date:
                messages.warning(self.request,"The coupon is yet to be available!")
                return redirect('cart-details')
            
            if cart.total() < coupon.required_amount_to_use_coupon:
                messages.warning(self.request,f"You have to shop at least{coupon.required_amount_to_use_coupon} to use this coupon code")
                return redirect('cart-details')
            
            cart.add_coupon(coupon.id)
            messages.success(self.request,"Your coupon has been applied successfully!")
            return redirect('cart-details')
        
        else:
            messages.error(self.request,"Invalid coupon code!")
            return redirect('cart-details')