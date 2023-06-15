from django.shortcuts import render
from .models import Products
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect 

# Create your views here.
def index(request):
    return render(
        request,
        'products/index.html',
        {'error': ""}
    )


@csrf_protect 
def findProduct(request):
    if request.method == 'POST':  
        sku = request.POST['SKU']
        products = Products.objects.filter(SKU__contains=f'{sku}').order_by('-ID')
        for product in products:
            images = product.Images
            break
        return render(
        request,
        'products/product.html',
        {'product': products, 'images': images.split(",")}
        )