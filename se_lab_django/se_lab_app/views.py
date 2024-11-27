from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal

def hello_world(request):
    return HttpResponse("Hello, World!")

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        name = data.get('name')
        price = data.get('price')
        available = data.get('available')

        if name is None or price is None or available is None:
            return HttpResponseBadRequest()

        product = Product(id=id,
                          name=name,
                          price=Decimal(str(price)),
                          available=available)

        try:
            product.full_clean()

        except Exception as e:
            print(e)
            return HttpResponseBadRequest()

        product.save()

        return JsonResponse({'id': product.id,
                                'name': product.name,
                                'price': float(product.price),
                                'available': product.available},
                            status=201)
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def product_detail(request, product_id):
    if request.method == 'GET':

        product = get_object_or_404(Product, id=product_id)

        return JsonResponse({'id': product.id,
                             'name': product.name,
                             'price': float(product.price),
                             'available': product.available})