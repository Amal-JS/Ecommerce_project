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

#display all products based on category , 
def category_display_all_products(request,category=None,sort_option=None):

    # brand = request.GET.get('brand')
    # category = request.GET.get('category')
    # sort_option = request.GET.get('sortby')
    print('brand : ', 'category : ', category, 'sort_option : ', sort_option)
    
    variants_with_images = Variant.objects.prefetch_related('variant_images').all().order_by('selling_price')

    if sort_option == 'price_high_to_low' or category== 'price_high_to_low':
        print('worked1')
        # Sort by price high to low (you may need to adjust this based on your model fields)

        variants_with_images = variants_with_images.order_by('-selling_price')

    elif sort_option == 'price_low_to_high' or category== 'price_low_to_high':
        print('worked2')
        # Sort by price low to high (you may need to adjust this based on your model fields)
        variants_with_images = variants_with_images.order_by('selling_price')

    
    if category != 'price_low_to_high' and category != 'price_high_to_low' and category is not None:
        print('worked3')
        if category and Category.objects.filter(name=category).exists():
            print('worked4')
            variants_with_images = variants_with_images.filter(product__category__name=category)
        else:
            print('worked5')
            variants_with_images = variants_with_images.filter(product__brand=category)

        

    return supporter_filter_sort(request,variants_with_images)

#supportor function for all products , category and products
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
def product(request):
    return render(request,'user_app/product.html')


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