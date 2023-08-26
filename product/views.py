from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    DetailView,
    ListView
)

from .models import (
    Category,
    Product,
    Slider
)


# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        context.update(
            {
                'featured_categories' : Category.objects.filter(featured=True),
                'featured_products' : Product.objects.filter(featured=True),
                'sliders' : Slider.objects.filter(show=True)
            }
        )
        return context

class ProductDetails(DetailView):
    model = Product
    template_name = 'product/product_details.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.get_object().related
        return context


class CategorytDetails(DetailView):
    model = Category
    template_name = 'product/category_details.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_object().products.all()
        return context
    
class ProductList(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)