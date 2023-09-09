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
#custom user model import
from . models import CustomUser

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
    items_per_page = 9  # Change this to your desired number

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

    return render(request,'user_app/user_sign_in.html',{'user_links':True})

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

    return render(request,'user_app/user_sign_up.html',{'user_links':True})


#function to handle user sign dynamic value checking

def user_sign_up_value(request):

    #getting the field name and value
    field_name = request.GET.get('field_name',None)
    field_value = request.GET.get('field_value',None)
    error_list=''
    print('comes')

    if field_name == 'username':


        if field_value == '':
            error_list += ',Username required'

        elif len(field_value)<5:
                error_list += ",Username atleast 5 characters"


        if len(field_value)>0 and  CustomUser.objects.filter(username=field_value).exists():
                    error_list = "Username already exists"

    #check email field
    elif field_name == 'email':

        if field_value == '':
            error_list += 'Email required'

        elif '@' not in field_value or '.' not in field_value:
            error_list += ",Enter valid Email"
        
        if len(field_value) >0 and CustomUser.objects.filter(email=field_value).exists():
            error_list += ",Email already exists"
        
           
    #phone field validation
    elif field_name == 'phone':

        if field_value == '':
            error_list += ',Phone Number required'
         
        elif len(str(field_value))>0 and len(str(field_value))<10:
            error_list += ",Phone Number must have 10 numbers"

        

        
        
    
    if error_list == '':  
        return JsonResponse({'exists':False})
    
        
    else:
        errors = { field_name:error_list }
        return JsonResponse({'exists':True,'errors':errors})

#logout user
def user_logout(request):
    logout(request)

    return redirect('user:index')