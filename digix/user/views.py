from django.shortcuts import redirect, render
#Form for user creation
from . forms import UserCreationForm
#display form validation errors
from django.contrib import messages
#check user authentication , login and logout (adding and removing user in session )
from django.contrib.auth import authenticate, login,logout
#import Variant model for index.html
from products.models import Variant

#home page
def index(request):
    variants_with_images = Variant.objects.prefetch_related('variant_images').all()
    return render(request,'user_app/home.html',{'variants_with_images':variants_with_images})

#display all products based on category , 
def category_display_all_products(request):
    return render(request,'user_app/category.html')

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