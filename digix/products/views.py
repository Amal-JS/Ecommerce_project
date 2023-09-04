from django.http import JsonResponse
from django.shortcuts import redirect, render
from . models import Category,Product,Variant



# these functions return the json response for data table 

def get_all_category(request):
    data= Category.objects.all().values()
    return JsonResponse({'data': list(data)})

def get_all_products(request):
    data= Product.objects.all().values()
    return JsonResponse({'data': list(data)})

def get_all_variants(request):
    data= Variant.objects.all().values()
    return JsonResponse({'data': list(data)})
