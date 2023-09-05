from django.shortcuts import redirect, render
from . forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

#home page
def index(request):
    return render(request,'user_app/home.html')

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