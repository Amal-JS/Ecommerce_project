from django.http import JsonResponse
from django.shortcuts import redirect, render
from . models import Category,Product,Variant



# these functions return the json response for data table 

def get_all_category(request):
    data= Category.objects.all().values()
    return JsonResponse({'data': list(data)})

def get_all_products(request):
    data = Product.objects.all().values('id', 'name', 'category__name','brand')
    
    print(list(data))
    return JsonResponse({'data': list(data)})

def get_all_variants(request):
    data= Variant.objects.all().values('id','name','product__name','ram','storage','color','mr_price','selling_price','stock','is_available')
    return JsonResponse({'data': list(data)})

def get_variant_data(request):
    

    variants = Variant.objects.all().prefetch_related('variant_images')
    
    data = []
    
    for variant in variants:
        variant_data = {
            'id': variant.id,
            'name': variant.name,
            'product_name': variant.product.name,
            'ram': variant.ram,
            'storage': variant.storage,
            'color': variant.color,
            'mr_price': variant.mr_price,
            'selling_price': variant.selling_price,
            'stock': variant.stock,
            'is_available': variant.is_available,
        }
        
        # Collect image URLs for the variant
        image_urls = [image.image.url for image in variant.variant_images.all()]
        
        variant_data['images'] = image_urls
        data.append(variant_data)
    
    return JsonResponse({'data': data})