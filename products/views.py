from django.shortcuts import render, HttpResponseRedirect
from products.models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required

def index(request):
    context = {
        "title": 'Store',
    }
    return render(request, 'products/index.html', context)

def products(request):
    context = {
        "title": 'Store - Каталог',
        "categories": ProductCategory.objects.all(),
        "products": Product.objects.all(),
    }
    return render(request, 'products/products.html', context)

@login_required
def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)
    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        basket = basket.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(current_page)

@login_required
def basket_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




# Create your views here.

