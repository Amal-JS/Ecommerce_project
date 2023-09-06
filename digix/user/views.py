from django.shortcuts import redirect, render
#Form for user creation
from . forms import UserCreationForm
#display form validation errors
from django.contrib import messages
#check user authentication , login and logout (adding and removing user in session )
from django.contrib.auth import authenticate, login,logout
#import Variant model for index.html
from products.models import Variant
#pagination
from django.core.paginator import Paginator

#home page
def index(request):
    variants_with_images = Variant.objects.prefetch_related('variant_images').all()
    return render(request,'user_app/home.html',{'variants_with_images':variants_with_images})

#display all products based on category , 
def category_display_all_products(request, category=None, brand=None):

    brand = request.GET.get('brand')
    category = request.GET.get('category')
    # Start with all variants with prefetch_related
    variants_with_images = Variant.objects.prefetch_related('variant_images').all()

    if category:
        # Filter by category name if category parameter is provided
        variants_with_images = variants_with_images.filter(product__category__name=category)

    if brand:
        # Filter by brand name if brand parameter is provided
        variants_with_images = variants_with_images.filter(product__brand=brand)

    if variants_with_images is None:
        print('empty')

     # Set the number of items per page
    items_per_page = 10  # Change this to your desired number

    # Create a Paginator object
    paginator = Paginator(variants_with_images, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(request, 'user_app/category.html', {'page': page})

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