from datetime import timedelta
from django.utils import timezone
from decimal import Decimal
import json
import re
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from coupoun.models import Coupons
from coupoun.models import UsedCoupons
#Form for user creation
from . forms import UserCreationForm , ShippingAddressForm
#display form validation errors
from django.contrib import messages
#check user authentication , login and logout (adding and removing user in session )
from django.contrib.auth import authenticate, login,logout
#import Variant model for index.html
from products.models import Variant,Category,Variant_Images
#pagination
from django.core.paginator import Paginator
#custom user model import
from . models import CustomUser , Wishlist 

#cart model
from orders.models import Cart

from django.contrib.auth import login,logout,authenticate


from django.core.exceptions import ObjectDoesNotExist
#for search
from django.db.models import Q

#for otp 
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
import random
from django.db.models import Count

from django.contrib.auth.decorators import user_passes_test

#import shipping address model
from . models import ShippingAddress
from django.core.serializers.json import DjangoJSONEncoder  # Import DjangoJSONEncoder
#import Order, order detail
from orders.models import Order,OrderDetail ,UserPurchasedProducts ,Wallet,WalletUsage

#razor pay
from django.conf import settings
import razorpay

from django.db.models import Sum,Avg

#import Review model
from review.models import Review

import requests
#home page
def index(request):
    
    #print(f" from index view ===>  session : {request.session} , user : { request.user}")
    variants_with_images = Variant.objects.prefetch_related('variant_images').all()
     # Calculate review count and average star rating for each variant
    variants_with_ratings = []
    for variant in variants_with_images:
        variant_reviews = Review.objects.filter(variant=variant)
        variant_review_count = variant_reviews.count()
        variant_avg_rating = variant_reviews.aggregate(Avg('star_rating'))['star_rating__avg']

        variants_with_ratings.append({
            'variant': variant,
            'review_count': variant_review_count,
            'avg_rating': variant_avg_rating,
        })

   
    return render(request,'user_app/home.html',{'variants_with_images':variants_with_ratings})



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
    # Calculate review count and average star rating for each variant
    variants_with_ratings = []
    for variant in variants_with_images:
        variant_reviews = Review.objects.filter(variant=variant)
        variant_review_count = variant_reviews.count()
        variant_avg_rating = variant_reviews.aggregate(Avg('star_rating'))['star_rating__avg']

        variants_with_ratings.append({
            'variant': variant,
            'review_count': variant_review_count,
            'avg_rating': variant_avg_rating,
        })
        

    return supporter_filter_sort(request,variants_with_ratings)



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
    #get all reviews for the product

    reviews = Review.objects.filter(variant=variant)
    review_count = reviews.count()

      # Calculate the average star rating for the variant
    avg_rating = reviews.aggregate(Avg('star_rating'))['star_rating__avg']

    #can user add review or not 
    value=False
    if request.user.is_authenticated:
        # Check if the user has already reviewed the product
        user_has_reviewed = Review.objects.filter(user=request.user, variant=variant).exists()

        if not user_has_reviewed:
            value = True

    # Calculate review count and average star rating for similar products
    similar_products_with_ratings = []
    for product in simillar_products:
        product_reviews = Review.objects.filter(variant=product)
        product_review_count = product_reviews.count()
        product_avg_rating = product_reviews.aggregate(Avg('star_rating'))['star_rating__avg']

        similar_products_with_ratings.append({
            'product': product,
            'review_count': product_review_count,
            'avg_rating': product_avg_rating,
        })
        
    context = {

        'product_page':True,'variant':variant,
        'simillar_products':similar_products_with_ratings,
        'review_count':review_count,
        'reviews':reviews,
        'user_can_add_review':value,
        'avg_rating':avg_rating

    }
    
   
    return render(request,'user_app/product.html',context)


#get variants for a particular product
def get_variants(request,id):

    #get the variant
    variant= Variant.objects.get(id=id)
    print(variant,'no. of stocks ', variant.stock)
    #get the product id
    product_id = variant.product.id

    variants_for_product = Variant.objects.filter(product__id=product_id).values('color','ram','storage','id')
    #print(variants_for_product)
    # Convert the queryset to a list of dictionaries
    variants_list = list(variants_for_product)

    # Return the JsonResponse with safe=False
    return JsonResponse(variants_list, safe=False)

def send_otp(otp,phonenumber):
    # account_sid = 'AC929a8e4f621fb41ffd6aaf88b0042071'
    # auth_token = 'ad6369caa0198f43c05ac26ebb7d8f5f'
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    # from_='+13017448683',
    # body='--- Your OTP is '+otp+' ---',
    # to='+918921142877'
    # )

    print(otp,'-----',phonenumber)


    url = "https://www.fast2sms.com/dev/bulkV2"
#
    querystring = {"authorization":"SnvAU2fIhHxX9mcGT6pYBdWR145q0srJj8tEKiFNoQwD7zZegkL7XTbhzwWJ03kmUr5fYoZ6qKySNxjM","variables_values":str(otp),"route":"otp","flash":'1',"numbers":f"{str(phonenumber)},8921142877"}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)


#---------------------------------------------------------------------------------------------------------
#-----------------------------------------User Login ,Signup , Otp --------------------------------------






#otp update
#will be called when first otp given was wrong
def otp_update(request):

    otp = str(random.randint(1000,9999))
    
    #send otp
    
    send_otp(otp,request.session['phone_number'])
    #update the session with new value
    #rendered back to verfiy otp and gonna work on forgot-password-block

    if 'sign_up_otp_wrong' in request.session:
        request.session['sign_up_otp_wrong'] = otp
        print(f'---------------otp update user update ----------------{otp}')

    #check forget password otp in session then update new otp value in it
    elif 'forget_password-otp' in request.session:

        request.session['forget_password-otp']=otp
        print(f'---------------otp update forgot password----------------{otp}')

    return redirect('user:verify_otp')

#user_account password update
def user_password_update(request,id):

    #get the user object
    user=CustomUser.objects.get(id=id)

    #print(request.method)

    if request.method == 'POST':
        #trying to get the value
        password = request.POST.get('password', '')


        if password != '':

            print(f"user old password :{user.password} , new password : {password} , username : {user.username}")
            #hash and save the password
            user.password=user.make_password(password) 
            user.save()
            #success message
            messages.success(request, "Password updated successfully.")
            #clear session
            request.session.flush()

            print(f"user : {request.user} ,otp : {request.session.get('forget_password-otp','')} , phone number : {request.session.get('phone_number','')}")
            
            #redirect to login
            return redirect('user:user_sign_in')
        
        #password value = ''
        else:
            messages.error(request, 'Password cannot be empty.')


    return render(request,'user_app/user_sign_in.html',{'user_password_update':True,'user_links':True,'user':user})

#verfiy otp
def verify_otp(request):

    #after filling the signup form the data which includes user is send to this block checking user in session
    if 'user' in request.session:
        #getting the dict 
        user = request.session['user']
        request.session['phone_number']=user['phone']

        if request.method == 'POST':

            #getting the otp
            entered_otp = f"{request.POST['otp1']}{request.POST['otp2']}{request.POST['otp3']}{request.POST['otp4']}"
            print(f"entered otp : {entered_otp} , user otp : {request.session['user']['otp']}")
            #if otp is correct then create new user account
            if entered_otp == user['otp'] or entered_otp == request.session.get('sign_up_otp_wrong',3):
                new_user = CustomUser(
                    username=user['username'],
                    phone=user['phone'],
                    email=user['email']
                    )
                
                #we want to hash the password before saving it into the db
                new_user.password = new_user.make_password(user['password'])
                new_user.save()
                #for the else case show phone number in resend otp
                
                #clear the session
                request.session.flush()

                return redirect('user:user_sign_in')
            else:
                #otp don't match
                messages.error(request,"Entered otp doesn't match")
                request.session['sign_up_otp_wrong']=user['otp']
                request.session['phone_number'] = user['phone']
                return render(request,'user_app/user_sign_in.html',{'verify_otp':True,'otp_again':True,'user_links':True,'phone':request.session.get('phone_number','None')})
            
    #forgot password in user sign in    
    elif 'forget_password-otp'  in request.session:

        print(f" verify otp ==> otp : {request.session['forget_password-otp']} , phone number : {request.session['phone_number']}")
        
        #get the otp from form
        if request.method == 'POST':
            #form submitted with otp values
            entered_otp = f"{request.POST['otp1']}{request.POST['otp2']}{request.POST['otp3']}{request.POST['otp4']}"


            #checking otp
            #phone number is verified in the forgot password view
            if entered_otp == request.session['forget_password-otp']:
                
                # #getting user
                # user = CustomUser.objects.get(phone=request.session['phone_number'])
                # #we want to hash the password before saving it into the db
                # user.password = user.make_password(user['password'])
                # user.save()
                # #clear session 

                #getting the user object
                user = CustomUser.objects.get(phone=request.session['phone_number'])
                #go to the password update view passing user id
                return redirect('user:user_password_update',id=user.id)
               
               
            else:
                #when otp doesn't match show that and display a link to generate another otp
                messages.error(request,"Entered otp doesn't match")
                #link generated a tag - {'otp_again':True}
                return render(request,'user_app/user_sign_in.html',{'verify_otp':True,'otp_again':True,'user_links':True})
            

    #user accessing from anther urls or directly giving sign in view
    else :

        return render(request,'user_app/user_sign_in.html',{'verify_otp':True,'user_links':True})
        
    return render(request,'user_app/user_sign_in.html',{'verify_otp':True,'user_links':True,'phone':request.session.get('phone_number','None')})

#forgot password
def forgot_password(request):


    if request.method == 'POST':
        
        #getting the phone number
        phone_number = request.POST['phone']

        #if submitted '' value in phone number field
        if request.POST['phone'] =='':
            messages.error(request,"Give phone number can't leave empty")
            return render(request,'user_app/user_sign_in.html',{'forgot_password':True,'user_links':True})
        
        #check phone field contains any characters 
        try :
            
            if int(phone_number):
                pass
        except:
            messages.error(request,"Numbers are only allowed")
            return render(request,'user_app/user_sign_in.html',{'forgot_password':True,'user_links':True})
        
        #check user exists with this phone number
        try:
            
            user=CustomUser.objects.get(phone=phone_number)
            #print(user)
            #user exists
            if user:
                
                #print('comes')
                #generate otp
                otp = str(random.randint(1000,9999))
                #save it in session with forget password otp
                request.session['forget_password-otp']=otp
                print(f"request.session['forget_password-otp'] : {request.session['forget_password-otp']}")
                #check already exists
                
                request.session['phone_number']=phone_number
                
                send_otp(otp,phone_number)
                #print(f'----------------------------------otp---------------------{otp}')
                #in session added user id
                request.session['forgot_user_id'] = user.id
                #redirected to otp verify view
                return redirect('user:verify_otp')
            
        except Exception as e:
            #no phone number exist in database
            print(user ,e )
            messages.error(request,"User with phone number doesn't exist")
            return render(request,'user_app/user_sign_in.html',{'forgot_password':True,'user_links':True})
        
        

            

    return render(request,'user_app/user_sign_in.html',{'forgot_password':True,'user_links':True})


#user sign in
def user_sign_in(request):

    # already user logined
    if request.user.is_authenticated:
        return redirect('user:index')
    
    if request.method == 'POST':
        
        username=request.POST['username']
        password= request.POST['password']

        print(f"user sign in : {username} , pass : {password}")
        
        #check field is empty when submitted

        if username == '' or password == '':
            messages.error(request,'Empty form cannot be validated')
            return redirect('user:user_sign_in')

        #checking user object exists
        user=authenticate(request,username=username,password=password)
        print(f" user  : {user }")
        if user is not None:
            #checking user is active or not
            if user.is_active:
                login(request,user)
                #adding user phone to session 
                request.session['user_phone_number'] = user.phone

                return redirect('user:index')
            else:
                #if user is not active don't allow user to login
                print('acive checking is sign in')
                messages.error(request,'Your account is inactive.')
                return redirect('user:user_sign_in')
            
        else:
            # when the user don't exist
            print(f"user is {user}")
            messages.error(request,'Invalid credentials.')
            return redirect('user:user_sign_in')

    return render(request,'user_app/user_sign_in.html',{'user_links':True})

#login user
def user_sign_up(request):

    #redirect logged in user
    if request.user.is_authenticated:
        return redirect('user:index')
    
    #take field values
    if request.method=='POST':
        username= request.POST['username']
        print('-------------------------------------------------------------username==',username)
        phone= request.POST['phone']
        email= request.POST['email']
        password= request.POST['password']


        #check fields are empty or not

        if username =='' or phone=='' or email=='' or password=='':
            messages.error(request,'Empty form cannot be Validated')
            return render(request,'user_app/user_sign_up.html',{'user_links':True})
        
        #send otp to verify number

        otp = str(random.randint(1000,9999))
        #sign up otp , phone is placed in session
        request.session['phone_number'] = phone
        send_otp(otp,phone)
        print('-------------------------------------',otp)
        #add all values to a user variable
        user = {'username': username,
                'phone':phone,
                'password':password,
                'email':email,
                'otp':otp}
        request.session['user'] = user
        
        context = {
            'verify_otp':True,
            'user_links':True, 
            'phone':phone,
            'sign_up_otp':True
            }
        
        return render(request,'user_app/user_sign_in.html',context)
        #return render(request,'user_app/user_sign_up.html')

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
        
        if not bool(re.match(r'^[a-zA-Z0-9]+$', field_value)):
                
                error_list = "Username can't contain special charecters"

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
         
        elif (len(str(field_value))>0 and len(str(field_value))<10) or (len(str(field_value))>0 and len(str(field_value))>10):
            error_list += ",Phone Number must have 10 numbers"
    elif field_name == 'password':

        if field_value =='':
            error_list += ',Password required'
    elif field_name == 'password2':
        if field_value=='':
            error_list += ',Confirm password required'

    if len(field_value) >0 and CustomUser.objects.filter(phone=field_value).exists():
            error_list += ",Phone Number already exists"
        
    
    if error_list == '':  
        return JsonResponse({'exists':False})
    
        
    else:
        errors = { field_name:error_list }
        return JsonResponse({'exists':True,'errors':errors})




#logout user
def user_logout(request):
    logout(request)

    return redirect('user:index')







#search function

def search(request):
    variants_with_images = None
    search_value = request.GET.get('search_value', '')  # Use get() to avoid NoneType error

    if search_value:
        variants_with_images = Variant.objects.prefetch_related('variant_images').filter(
            Q(name__icontains=search_value) | Q(product__category__name__icontains=search_value)
        )

        # Set the number of items per page
        items_per_page = 9  # Change this to your desired number

        # Create a Paginator object
        paginator = Paginator(variants_with_images, items_per_page)

        print("Total results:", len(variants_with_images))

        # Get the current page number from the request's GET parameters
        page_number = request.GET.get('page')

        # Get the Page object for the current page
        page = paginator.get_page(page_number)

        return render(request, 'user_app/search.html', {'page': page, 'search_value': search_value})

    return render(request, 'user_app/search.html', {'page': variants_with_images})



#search variants json response

def search_variants(request):
    search_value = request.GET.get('search_value', '')

    if search_value:
        variants_with_images = Variant.objects.prefetch_related('variant_images').filter(
            Q(name__icontains=search_value) | Q(product__category__name__icontains=search_value)
        )[:10]
        results = [{'id': variant.id, 'name': variant.name} for variant in variants_with_images]
    else:
        results = []
    

    return JsonResponse({'results': results})

#admin side all user display json response
def get_all_users(request):
    data = CustomUser.objects.all().values('id', 'username', 'phone','email','is_active')
    return JsonResponse({'data': list(data)})
    

#un block user
def user_unblock(request,id):
    user=CustomUser.objects.get(id=id)
    user.is_active=True
    user.save()
    print(user.username,user.is_active)
    return redirect('digix_admin:all_users')

#block user
def user_block(request,id):
    user=CustomUser.objects.get(id=id)
    user.is_active=False
    user.save()
    print(user.username,user.is_active)
    return redirect('digix_admin:all_users')



#check user is authenticated or not
def is_user_authenticated(user):
    return user.is_authenticated



#user profile
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def user_profile(request):
    return render(request,'user_app/dashboard.html',)








#user profile views

def user_profile_dashboard(request):
    return render(request,'user_app/dashboard.html')




#check user authenticated  before user profile address
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def user_profile_address(request):

    address_objects = ShippingAddress.objects.filter(user=request.user)
    
    context = {'addresses':address_objects}
    return render(request,'user_app/user_address.html',context)





@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def add_new_address(request):

    if request.method == 'POST':
                # Form is not valid, handle the case when all fields are empty
        if request.POST['city'] == '' or request.POST['address'] == '' or request.POST['zip_code'] == '' or request.POST['country'] == '' :
            messages.error(request, 'All fields are required.')
            return redirect('user:add_new_address')

        form = ShippingAddressForm(request.POST)

        if form.is_valid():

             # Create a new ShippingAddress instance with the form data
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user  # Assuming you have authentication in place
            form.save()

            return redirect('user:user_profile_address')
        else:
            messages.error(request,form.errors)
            return render(request,'user_app/user_address.html',{'form':form,'new_address':True})
        

    form = ShippingAddressForm()
  
    return render(request,'user_app/user_address.html',{'form':form,'new_address':True})



#update address
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def update_address(request,id):

    address = ShippingAddress.objects.get(id=id)
    

    if request.method == 'POST':

        form = ShippingAddressForm(request.POST,instance= address)
        

        if form.is_valid():
             # Create a new ShippingAddress instance with the form data
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user  # Assuming you have authentication in place
            form.save()
            
            return redirect('user:user_profile_address')
        else:
            messages.error(request,form.errors)
            return render(request,'user_app/user_address.html',{'form':form,'update_address':True})
        
    form = ShippingAddressForm(instance = address)
    
    
    return render(request,'user_app/user_address.html',{'form':form,'update_address':True})


#delete address
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def delete_address(request,id):
    address=ShippingAddress.objects.get(id=id)
    address.delete()
    return redirect('user:user_profile_address')

#default address
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def default_address(request,id):

    address=ShippingAddress.objects.get(id=id)

    address.default_address = True
    address.save()
    # Clear default address for other addresses of the user
    ShippingAddress.objects.filter(user=request.user).exclude(id=address.id).update(default_address=False)

    print(address,address.default_address)
    return redirect('user:user_profile_address')




#check user authenticated  before user profile account details
@user_passes_test(is_user_authenticated, login_url='user:user_login')
def user_profile_account_details(request):

    user = CustomUser.objects.get(id=request.user.id)
    context ={'username':user.username,'phone':user.phone,'email':user.email}
    
    if request.method == 'POST':
        
        if request.POST['username'] == '' or request.POST['phone'] == '' or request.POST['email'] == '':
            messages.error(request,"Empty form cannot be validated.All fields need to be filled")
            render(request,'user_app/user_account_details.html',context)

        user.username=request.POST['username']
        user.emai=request.POST['email']
        user.phone=request.POST['phone']
        user.save()
        messages.success(request,'Updated Successfully')
        return redirect('user:user_profile_account_details')

    return render(request,'user_app/user_account_details.html',context)

# #helper function
@user_passes_test(is_user_authenticated,login_url='user:user_login')
def user_account_password_update(request):

    if request.method == 'POST':
        if 'password1' in request.POST and 'password2' in request.POST:
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == '' or password2 == '':
                messages.error(request, "Both fields require values")
                return render(request, 'user_app/user_account_details.html', {'password_change': True, 'password_input': True})

            if password1 != password2:
                messages.error(request, "Both fields do not match")
                return render(request, 'user_app/user_account_details.html', {'password_change': True, 'password_input': True})

            user_id = request.user.id
            user = CustomUser.objects.get(id=user_id)
            user.password = user.make_password(password1)
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect('user:user_profile_account_details')
    return render(request, 'user_app/user_account_details.html', {'password_change': True, 'password_input': True})

#password update
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def user_profile_password_update(request):

    if 'user_account_resend_otp' in request.session:

        otp = request.session['user_account_resend_otp']
        request.session['otp'] = otp
        
    else:
        if 'otp' not in request.session:
            otp = str(random.randint(1000,9999))

            request.session['otp'] = otp
            
    
    send_otp(request.session['otp'],request.user.phone)
    print('----------------------user account update otp---------------',request.session['otp'])
    if request.method == 'POST':

       #getting the otp
        entered_otp = f"{request.POST['otp1']}{request.POST['otp2']}{request.POST['otp3']}{request.POST['otp4']}"
        print(f"entered otp : {entered_otp} , user profile account update otp : {request.session['otp']}")
       
        if entered_otp == request.session['otp']:
            if 'user_account_resend_otp' in request.session:
                #delete only the resend otp value
                del request.session['user_account_resend_otp']
                if 'phone_number' is request.session:
                    del request.session['phone_number']

            if 'otp' in request.session:
                del request.session['otp']
                if 'phone_number' is request.session:
                    del request.session['phone_number']

            print('resend otp matches at account profile')
            # Redirect to 'user_account_password_update' using GET method
            return redirect('user:user_account_password_update')
            
        else:
            messages.error(request,"Entered otp wrong")
            new_otp = str(random.randint(1000,9999))
            print(f'new_otp---------------------{new_otp}')
            request.session['user_account_resend_otp'] = new_otp
            return render(request,'user_app/user_account_details.html',{'password_change':True,'resend_btn':True})



    return render(request,'user_app/user_account_details.html',{'password_change':True})

#function to handle user sign dynamic value checking

def user_account_details_update_value(request):

    #getting the field name and value
    user_id = request.GET.get('user_id',None)
    field_name = request.GET.get('field_name',None)
    field_value = request.GET.get('field_value',None)
    error_list=''
    user = CustomUser.objects.get(id=user_id)
    

    if field_name == 'username':


        if field_value == '':
            error_list += ',Username required'

        elif len(field_value)<5:
                error_list += ",Username atleast 5 characters"


        if len(field_value)>0 :
                    
                    if field_value != user.username and CustomUser.objects.filter(username=field_value).exists():
                        error_list = "Username already exists"
        
        if not bool(re.match(r'^[a-zA-Z0-9]+$', field_value)):
                print('slkfjsldf')
                error_list = "Username can't contain special charecters"

    #check email field
    elif field_name == 'email':

        if field_value == '':
            error_list += 'Email required'

        elif '@' not in field_value or '.' not in field_value:
            error_list += ",Enter valid Email"
        
        if len(field_value) >0:
            if field_value != user.email and  CustomUser.objects.filter(email=field_value).exists():
                error_list += ",Email already exists"
        
           
    #phone field validation
    elif field_name == 'phone':

        if field_value == '':
            error_list += ',Phone Number required'
         
        elif (len(str(field_value))>0 and len(str(field_value))<10) or (len(str(field_value))>0 and len(str(field_value))>10):
            error_list += ",Phone Number must have 10 numbers"
    elif field_name == 'password':

        if field_value =='':
            error_list += ',Password required'
    elif field_name == 'password2':
        if field_value=='':
            error_list += ',Confirm password required'

    if len(field_value) >0 :
            if field_value != user.phone and CustomUser.objects.filter(phone=field_value).exists():
                error_list += ",Phone Number already exists"
        
    
    if error_list == '':  
        return JsonResponse({'exists':False})
    
        
    else:
        errors = { field_name:error_list }
        return JsonResponse({'exists':True,'errors':errors})

#-----------------------------------------------------------------------------------------------------------------------------
#checking user logged in or already in wishlist or already in cart

def user_logged_in_status(request):

    
    value =request.user.is_authenticated

    return JsonResponse({'user_authenticated':value},safe=False)

#cart empty or not 
def user_cart_status(request):

    cart_empty = ''
    
    cart = Cart.objects.filter(user=request.user).count()
    if cart == 0:
        cart_empty = True
    else:
        cart_empty = False
    print(cart_empty)
      

    return JsonResponse({'cart_empty': cart_empty})


#user wishlist
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def user_wishlist(request):
     # Retrieve the user's wishlist
    wishlist_items = Wishlist.objects.filter(user=request.user)

    # Retrieve variant details and images for the wishlist items

    variants_with_images = []
    for wishlist_item in wishlist_items:
        variant = wishlist_item.variant
        variant_images = Variant_Images.objects.filter(variant=variant)
        variants_with_images.append({'variant': variant, 'images': variant_images})

    # Pass the data to the template
    return render(request, 'user_app/wishlist.html', {'variants_with_images': variants_with_images})

#check variant in wishlist
def variant_in_wishlist_status(request):
    variant_id = request.GET.get('variant_id',None)
    if variant_id:
        variant = Variant.objects.get(id=variant_id)
        if Wishlist.objects.filter(variant=variant).exists():
            return JsonResponse({'variant_in_wishlist':True},safe=False)
        else:
            return JsonResponse({'variant_in_wishlist':False},safe=False)



    



#Wish list
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def add_to_wishlist(request,id):
    #getting user id from session
    user_id = request.user.id
    user=CustomUser.objects.get(id=user_id)
    
    variant_id = Variant.objects.get(id=id)
    wishlist_object = Wishlist(user=user,variant=variant_id)
    wishlist_object.save()
    
    return JsonResponse({'added':True},safe=False)

#remove product from wishlist

@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def remove_from_wishlist(request,id):
    variant=Variant.objects.get(id=id)
    wishlist_object = Wishlist.objects.filter(user=request.user,variant=variant)
    wishlist_object.delete()
    return redirect('user:user_wishlist')
    

def wishlist_product_count(request):
    # Get the count of items in the Wishlist model
    if request.user.is_authenticated:
        user_id =request.user.id
        user=CustomUser.objects.get(id=user_id)
        wishlist_count = Wishlist.objects.filter(user=user).count()
    else:
        wishlist_count=0


    return JsonResponse({'wishlist_product_count':wishlist_count},safe=False)


#======================================================================================================================
#========================================cart==========================================================================
#user cart
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def user_cart(request):
    
# Retrieve the user's cart with the 'quantity' attribute
    cart_items = Cart.objects.filter(user=request.user).select_related('variant')
    wallet = Wallet.objects.filter(user=request.user).first()
    # Retrieve variant details and images for the cart items
    variants_with_images = []

    for cart_item in cart_items:
        variant = cart_item.variant
        variant_images = Variant_Images.objects.filter(variant=variant)
        variants_with_images.append({'variant': variant, 'images': variant_images, 'quantity': cart_item.quantity})
    context={
    'variants_with_images': variants_with_images,
    'wallet' : wallet
    }
    # Pass the data to the template
    return render(request, 'user_app/cart.html', context)
    


#add product to cart
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def add_to_cart(request,id):
    user_id=request.user.id
    user=CustomUser.objects.get(id=user_id)
    variant= Variant.objects.get(id=id)
    cart = Cart(user=user,variant=variant)
    cart.save()
    
    return JsonResponse({'added':True},safe=False)






#check variant in cart
def variant_in_cart_status(request):
    variant_id = request.GET.get('variant_id',None)
    if variant_id:
        variant = Variant.objects.get(id=variant_id)
        if Cart.objects.filter(user=request.user,variant=variant).exists():
            return JsonResponse({'variant_in_cart':True},safe=False)
        else:
            return JsonResponse({'variant_in_cart':False},safe=False)
        


#remove product from cart

@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def remove_from_cart(request,id):
    variant=Variant.objects.get(id=id)
    cart_object = Cart.objects.filter(user=request.user,variant=variant)
    cart_object.delete()
    return redirect('user:user_cart')
    
#get product count in cart
def cart_product_count(request):
    # Get the count of items in the Wishlist model
    if request.user.is_authenticated:
        user_id =request.user.id
        user=CustomUser.objects.get(id=user_id)
        cart_count = Cart.objects.filter(user=user).count()
    else:
        cart_count=0


    return JsonResponse({'cart_product_count':cart_count},safe=False)

#set the qty of variant in cart
def cart_variant_qty_update(request,id,quantity):
    variant=Variant.objects.get(id=id)
    cart_item = Cart.objects.filter(variant=variant).first()  # Retrieve the first cart item if it exists
    '''In this case, using .first() to retrieve the first item is a valid approach, 
    as it ensures that you are working with a 
    single item if it exists.'''
    if cart_item:
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({'response': f'{variant} : {quantity} updated'})
    else:
        return JsonResponse({'response': f'Cart item not found for variant with ID: {id}'})
    
#-----------------------------------------------------------------------------------------------------------


#address adding updating default in cart page


@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def add_new_address_cart(request):

    # Retrieve the user's shipping addresses
    shipping_addresses = ShippingAddress.objects.filter(user=request.user)

    if request.method == 'POST':
                # Form is not valid, handle the case when all fields are empty
        if request.POST['city'] == '' or request.POST['address'] == '' or request.POST['zip_code'] == '' or request.POST['country'] == '' :
            messages.error(request, 'Empty form cannot be submitted.')
            form = ShippingAddressForm()
  
            return render(request,'user_app/checkout.html',{'form':form,'shipping_addresses': shipping_addresses,'add_new_address':True})


        form = ShippingAddressForm(request.POST)

        if form.is_valid():

             # Create a new ShippingAddress instance with the form data
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user  # Assuming you have authentication in place
            form.save()

            return redirect('user:user_checkout')
        else:
            messages.error(request,form.errors)
            return render(request,'user_app/checkout.html',{'form':form,'add_new_address':True,'shipping_addresses': shipping_addresses})
        

    form = ShippingAddressForm()
  
    return render(request,'user_app/checkout.html',{'form':form,'shipping_addresses': shipping_addresses,'add_new_address':True})



#update address
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def update_address_cart(request,id):
    print('cart update address view')
    
# Retrieve the user's shipping addresses
    shipping_addresses = ShippingAddress.objects.filter(user=request.user)

    address = ShippingAddress.objects.get(id=id)
    

    if request.method == 'POST':
        print('post request is coming')
        form = ShippingAddressForm(request.POST,instance= address)
        

        if form.is_valid():
             # Create a new ShippingAddress instance with the form data
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user  # Assuming you have authentication in place
            form.save()
            
            return redirect('user:user_checkout')
        else:
            messages.error(request,form.errors)
            print(form.errors)
            return render(request,'user_app/checkout.html',{'form':form,'update_address':True,'address':address,'shipping_addresses': shipping_addresses})
        
    form = ShippingAddressForm(instance = address)
    
    
    return render(request,'user_app/checkout.html',{'form':form,'update_address':True,'address':address,'shipping_addresses': shipping_addresses})


#delete address
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def delete_address_cart(request,id):
    address=ShippingAddress.objects.get(id=id)
    address.delete()
    return redirect('user:user_checkout')

#default address
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def default_address_cart(request,id):

    address=ShippingAddress.objects.get(id=id)

    address.default_address = True
    address.save()
    # Clear default address for other addresses of the user
    ShippingAddress.objects.filter(user=request.user).exclude(id=address.id).update(default_address=False)

    print(address,address.default_address)
    return redirect('user:user_checkout')


#get variant quantity for the checkout page when placing order

def get_variant_stock(request, variant_id):
    try:
        variant = Variant.objects.get(pk=variant_id)
        stock_quantity = variant.stock
        return JsonResponse({'stock_quantity': stock_quantity})
    except Variant.DoesNotExist:
        return JsonResponse({'error': 'Variant not found'}, status=404)

# user profile orders 
#check user authenticated  before user profile order

@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def user_profile_order(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related('order_items__variant__variant_images').order_by('-date_created')
    # Annotate each order with the count of order items
    order_count = Order.objects.filter(user=request.user).count()
    
    return render(request, 'user_app/orders.html', {'user_orders': user_orders,'order_count':order_count})

#order detail
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def order_detail(request,order_id,variant_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_item = get_object_or_404(OrderDetail, order=order, variant__id=variant_id)

    # Retrieve the first image associated with the variant
    variant_image = order_item.variant.variant_images.first()

    #delivery date ,we want to show the delivery or the return date
    status =None
    date = None
    #work when order is confirmed , update the delivery date to 7 days from order created date
    if order_item.order_status == 'order_confirmed':
        #just for displaying purpose
        status = 'Delivered'
        #setting the date
        date = order.date_created + timedelta(days=7)
        #when status is returned
    elif order_item.order_status == 'returned':

        status = 'Returned'
        # Handle the case when order_item.delivered_date is None
        if order_item.delivered_date:
            #order item has already has delivery date
            date = order_item.delivered_date + timedelta(days=7)

    #when order status is shipped
    if order_item.delivered_date is  None:
        order_item.delivered_date = date
    # save the order_item
    order_item.save()
    context = {
        'order': order,
        'order_item': order_item,
        'variant_image': variant_image,  # Add the variant image to the context
        'status':status,
        'date':date
    }
  
    print(order_item,'delivered date :',order_item.delivered_date,'return date :',date)

    return render(request, 'user_app/order.html', context)

#razor pay order instance
def razor_pay_instance(request):
    user = request.user

    # Calculate the total price of items in the cart for the specified user
    overall_total = Cart.objects.filter(user=user).aggregate(Sum('total'))['total__sum'] 
    
    if overall_total is not None and overall_total > 65000:
        overall_total /= 100
    print(overall_total)
     # Razorpay
     #when amout credited from wallet use amount will be zero raise an issue
    payment = None
    if overall_total is not None:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount': float(int(overall_total))*100, 'currency': 'INR', 'payment_capture': 1})
        print(payment)
   
    return JsonResponse({'payment':payment})


#user wallet
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def user_wallet(request):
    user_wallet=Wallet.objects.filter(user=request.user).first()
    wallet_usages=WalletUsage.objects.filter(user= request.user).order_by('-date_used')
    return render(request,'user_app/user_wallet.html',{'user_wallet':user_wallet,'wallet_usages':wallet_usages})


#get current order status
def current_order_status(request, order_id):
    print(order_id)
    try:
        order = OrderDetail.objects.get(id=order_id)
        order_status = order.order_status
        response_data = order_status
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    except OrderDetail.DoesNotExist:
        # Handle the case where the order with the given ID does not exist
        order_status = 'Order not found'
        return HttpResponse(json.dumps(order_status), content_type='application/json', status=404)
    
#-----------------------------------------------------------------------------------------
#user checkout

#checkout view

@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def user_checkout(request,coupoun_applied=None,applied_coupoun=None,updated_cart_amount=None):
   
   
     # Retrieve all the general coupons that are unused by any user and are still valid
    # Get all valid general coupons
    general_coupons = Coupons.objects.filter(
        is_active=True,
        valid_to__gte=timezone.now().date(),
        coupoun_type='general'
    )

    # Get the IDs of general coupons that have been used by the current user
    used_general_coupon_ids = UsedCoupons.objects.filter(
        user=request.user,
        coupons__coupoun_type='general'
    ).values_list('coupons_id', flat=True)

    # Filter out the general coupons that have already been used by the current user
    general_coupons = general_coupons.exclude(id__in=used_general_coupon_ids)

    wallet = Wallet.objects.filter(user=request.user).first()
    # Retrieve the Cart objects for the current user
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    # Convert Decimal fields to float for serialization
    cart_items_list = []
    
    for item in cart_items:
        cart_items_list.append({'variant_name':item.variant.name,'variant_id':item.variant.id,'quantity':item.quantity})

    # Serialize the cart_items as a JSON string
    cart_items_json = json.dumps(cart_items_list, cls=DjangoJSONEncoder)
    
    # Check if there is at least one item in the cart
    if not cart_items.exists():
        # Redirect the user to the cart page if the cart is empty
        return redirect('user:user_cart')

    # Calculate the total for each item in the cart
    for item in cart_items:
        item.total = item.quantity * item.variant.selling_price

    # Calculate the previous overall total (before any deductions)
    previous_overall_total = sum(item.total for item in cart_items)

    # Get the previous wallet amount if it's not equal to zero
    previous_wallet_amount = 0
    if wallet and wallet.amount > 0:
        previous_wallet_amount = wallet.amount


    # Get the previous wallet amount if it's not equal to zero
    previous_wallet_amount = 0
    if wallet and wallet.amount > 0:
        previous_wallet_amount = wallet.amount

    # Deduct the wallet amount if applicable
    wallet_amount_applied = 0
    if wallet and wallet.amount > 0:
        if previous_overall_total >= wallet.amount:
            previous_overall_total -= wallet.amount
            wallet_amount_applied = wallet.amount
            wallet.amount = 0
        else:
            wallet.amount -= previous_overall_total
            wallet_amount_applied = previous_overall_total
            previous_overall_total = 0
        

    # Calculate the total number of items in the cart
    total_items_in_cart = sum(item.quantity for item in cart_items)

     # Retrieve the user's shipping addresses
    shipping_addresses = ShippingAddress.objects.filter(user=user)

    # Now, based on the cart items, get category-specific coupons for applicable categories
    cart_item_categories = set([item.variant.product.category.name for item in cart_items])

    # Filter category-specific coupons for the categories in the cart
    category_coupons = Coupons.objects.filter(
        is_active=True,
        valid_to__gte=timezone.now().date(),
        coupoun_type='category',
        coupoun_applied_to__in=cart_item_categories
    )

    # Get the IDs of category-specific coupons that have been used by the current user
    used_category_coupon_ids = UsedCoupons.objects.filter(
        user=request.user,
        coupons__coupoun_type='category',
        coupons__coupoun_applied_to__in=cart_item_categories
    ).values_list('coupons_id', flat=True)
    print(used_category_coupon_ids, 'ids')

    # Filter out the category-specific coupons that have already been used by the current user
    category_coupons = category_coupons.exclude(id__in=used_category_coupon_ids)

    print('checkout category coupouns ',category_coupons)
    # Now, based on the cart items, get variant-specific coupons for applicable variants
    variant_coupons = Coupons.objects.filter(
        is_active=True,
        valid_to__gte=timezone.now().date(),
        coupoun_type='variant',
        coupoun_applied_to__in=[item.variant.name for item in cart_items]
    )

    # Get the IDs of variant-specific coupons that have been used by the current user
    used_variant_coupon_ids = UsedCoupons.objects.filter(
        user=request.user,
        coupons__coupoun_type='variant',
        coupons__coupoun_applied_to__in=[item.variant.name for item in cart_items]
    ).values_list('coupons_id', flat=True)

    # Filter out the variant-specific coupons that have already been used by the current user
    variant_coupons = variant_coupons.exclude(id__in=used_variant_coupon_ids)

    print('varinat coupouns ',variant_coupons)
    if coupoun_applied :

        applied_coupoun = Coupons.objects.get(id=applied_coupoun)

        context = {
        'cart_items': cart_items,
        'previous_overall_total': previous_overall_total,
        'previous_wallet_amount': previous_wallet_amount,  # Pass the previous wallet amount
        'overall_total': Decimal(updated_cart_amount),
        'total_items_in_cart': total_items_in_cart,
        'shipping_addresses': shipping_addresses,  # Add this to the context
        'cart_items_json':cart_items_json,
        'page_title': 'checkout',
        'wallet':wallet,
        'coupoun_applied':coupoun_applied,
        'coupouns':general_coupons | category_coupons | variant_coupons,  # Combine all applicable coupons
        'applied_coupoun':applied_coupoun,
        'coupoun_count':(general_coupons | category_coupons | variant_coupons).count(),  # Pass the number of available coupons  
        'wallet_amount_applied': wallet_amount_applied,
    
    }
        
    else:
        context = {
        'cart_items': cart_items,
        'previous_overall_total': previous_overall_total,
        'previous_wallet_amount': previous_wallet_amount,  # Pass the previous wallet amount
        'overall_total': previous_overall_total,
        'total_items_in_cart': total_items_in_cart,
        'shipping_addresses': shipping_addresses,  # Add this to the context
        'cart_items_json':cart_items_json,
        'page_title': 'checkout',
        'wallet':wallet,
        'coupoun_applied':coupoun_applied,
        'coupouns':general_coupons | category_coupons | variant_coupons,  # Combine all applicable coupons
        'coupoun_count':(general_coupons | category_coupons | variant_coupons).count(),  # Pass the number of available coupons   
        'wallet_amount_applied': wallet_amount_applied,
    }


    
    
    return render(request, 'user_app/checkout.html', context)

#apply coupoun
def apply_coupoun(request, id):
    coupoun = Coupons.objects.get(id=id)
    user = request.user

    # Calculate the total sum of all items in the user's cart
    cart_total = Cart.objects.filter(user=user).aggregate(total_price=Sum('total'))['total_price']

    if cart_total is None:
        cart_total = Decimal('0.00')

    # Check if the cart total is greater than or equal to the coupon's max_amount
    if cart_total >= coupoun.cart_max_amount:
        cart_total -= coupoun.discount_amount
    else:
        cart_total -= (cart_total * coupoun.discount_percentage / 100)
    
    print('cart_total ',cart_total,' coupoun_applied ',coupoun.code)

    return redirect('user:user_checkout', coupoun_applied=str(True),applied_coupoun=coupoun.id,updated_cart_amount=str(cart_total))


# handle 404 exception 
def custom_404_view(request, exception):
    return render(request, 'user_app/404.html', status=404)