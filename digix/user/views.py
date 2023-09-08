from django.http import JsonResponse
from django.shortcuts import redirect, render
#Form for user creation
from . forms import UserCreationForm
#display form validation errors
from django.contrib import messages
#check user authentication , login and logout (adding and removing user in session )
from django.contrib.auth import authenticate, login,logout
#import Variant model for index.html
from products.models import Variant,Category
#pagination
from django.core.paginator import Paginator

#home page
def index(request):
    variants_with_images = Variant.objects.prefetch_related('variant_images').all()
    return render(request,'user_app/home.html',{'variants_with_images':variants_with_images})

#display all products based on category , brand
def category_display_all_products(request,category=None,sort_option=None):

    filter_value=category
 
    #print('brand : ', 'category : ', category, 'sort_option : ', sort_option)
    
    variants_with_images = Variant.objects.prefetch_related('variant_images').all()

    #why filter_value == price high to low , this view also handles all products functionallity
    if sort_option == 'price_high_to_low' or filter_value== 'price_high_to_low':
        #print('worked1')
        # Sort by price high to low (you may need to adjust this based on your model fields)
        #desc - '-selling_price'
        variants_with_images = variants_with_images.order_by('-selling_price')

#why filter_value == price high to low , this view also handles all products functionallity
    elif sort_option == 'price_low_to_high' or filter_value== 'price_low_to_high':
        #print('worked2')
        # Sort by price low to high (you may need to adjust this based on your model fields)
        variants_with_images = variants_with_images.order_by('selling_price')

    #filter value now contains either category name or brand name
    if filter_value != 'price_low_to_high' and filter_value != 'price_high_to_low' and filter_value is not None:
        #print('worked3')
        #check if filter value is a category or not ,true if it is category
        if filter_value and Category.objects.filter(name=filter_value).exists():
            #print('worked4')
            variants_with_images = variants_with_images.filter(product__category__name=filter_value)
        else:
            #print('worked5')
            #filter value with brand name
            variants_with_images = variants_with_images.filter(product__brand=filter_value)

        

    return supporter_filter_sort(request,variants_with_images)



#supportor function for all products , filter_value and products
def supporter_filter_sort(request,variants_with_images):

     # Set the number of items per page
    items_per_page = 10  # Change this to your desired number

    # Create a Paginator object
    paginator = Paginator(variants_with_images, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)
    return render(request,'user_app/category.html',{'page': page})


#display single product
def product(request,id):
    variant = Variant.objects.prefetch_related('variant_images').get(id=id)
    simillar_products = Variant.objects.prefetch_related('variant_images').filter(product__category__name=variant.product.category.name)[:8]
    return render(request,'user_app/product.html',{'product_page':True,'variant':variant,'simillar_products':simillar_products})


#get variants for a particular product
def get_variants(request,id):

    #get the variant
    variant= Variant.objects.get(id=id)
    print(variant)
    #get the product id
    product_id = variant.product.id

    variants_for_product = Variant.objects.filter(product__id=product_id).values('color','ram','storage','id')
    print(variants_for_product)
    # Convert the queryset to a list of dictionaries
    variants_list = list(variants_for_product)

    # Return the JsonResponse with safe=False
    return JsonResponse(variants_list, safe=False)


#user sign in
def user_sign_in(request):
    if request.method == 'POST':
        username=request.POST['username']
        password= request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('user:index')
        else:
            messages.error(request,'invalid credentials')
            return redirect('user:user_sign_in')

    return render(request,'user_app/user_sign_in.html')

#login user
def user_sign_up(request):

    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            return redirect('user:index')
        else:
            messages.error(request,form.errors)
            return render(request,'user_app/user_sign_up.html')
    form = UserCreationForm()

    return render(request,'user_app/user_sign_up.html')


#logout user
def user_logout(request):
    logout(request)

    return redirect('user:index')