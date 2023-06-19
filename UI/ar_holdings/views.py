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
        ##colors = ""
        colors = []
        images = ""

        if not products:
            return redirect('index')

        ##Slower metod but fixes the case on edge case WSH12
        for product in products:

            ##Get the images of the variable SKU that will be the first one
            if images == "":
                images = product.Images

            ##Get the colors oyt of the variants by going through them
            if product.Type == 'variation' and '|' not in product.Attribute_2_value:

                ##If color not already append then append it
                if product.Attribute_2_value not in colors:
                    colors.append(product.Attribute_2_value)


        color_stylings= []
        
        ##Create the style for every button and add the JS function too
        for color in colors:
            color_stylings.append(f'''style="background-color: {color.lower()} !important;
                                      border-radius:55px;
                                      height: 35px;
                                      margin-left:10px;" onclick="changeImg('{color.lower()}')"''')

        return render(
        request,
        'products/product.html',
        {'product': products, 'images': images.split(","), 'colors':color_stylings}
        )