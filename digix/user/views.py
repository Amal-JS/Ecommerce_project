from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'user_app/home.html')


def category_display_all_products(request):
    return render(request,'user_app/category.html')

def product(request):
    return render(request,'user_app/product.html')