import re
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
#Form for user creation
from . forms import UserCreationForm , ShippingAddressForm
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


from django.contrib.auth import login,logout,authenticate


from django.core.exceptions import ObjectDoesNotExist
#for search
from django.db.models import Q

#for otp 
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
import random


from django.contrib.auth.decorators import user_passes_test

#import shipping address model
from . models import ShippingAddress




#home page
def index(request):

    #print(f" from index view ===>  session : {request.session} , user : { request.user}")
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
    print(variant,'no. of stocks ', variant.stock)
    #get the product id
    product_id = variant.product.id

    variants_for_product = Variant.objects.filter(product__id=product_id).values('color','ram','storage','id')
    #print(variants_for_product)
    # Convert the queryset to a list of dictionaries
    variants_list = list(variants_for_product)

    # Return the JsonResponse with safe=False
    return JsonResponse(variants_list, safe=False)

def send_otp(otp):
    account_sid = 'AC929a8e4f621fb41ffd6aaf88b0042071'
    auth_token = 'bf99032ef3ee29284d3118533ccc4c67'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+13017448683',
    body='--- Your OTP is '+otp+' ---',
    to='+918921142877'
    )

    print(message.sid)


#---------------------------------------------------------------------------------------------------------
#-----------------------------------------User Login ,Signup , Otp --------------------------------------



#otp update
#will be called when first otp given was wrong
def otp_update(request):

    otp = str(random.randint(1000,9999))
    
    #send otp
    
    send_otp(otp)
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
                
                send_otp(otp)
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
        send_otp(otp)
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
                print('slkfjsldf')
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
def user_profile(request):
    return render(request,'user_app/dashboard.html',)


#user wishlist
def user_wishlist(request):
    return render(request,'user_app/wishlist.html')

#user cart
def user_cart(request):
    return render(request,'user_app/cart.html')

#user checkout
def user_checkout(request):
    return render(request,'user_app/checkout.html')



#user profile views

def user_profile_dashboard(request):
    return render(request,'user_app/dashboard.html')


#check user authenticated  before user profile order
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def user_profile_order(request):
    return render(request,'user_app/orders.html')


#check user authenticated  before user profile address
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def user_profile_address(request):

    address_objects = ShippingAddress.objects.all()
    
    context = {'addresses':address_objects}
    return render(request,'user_app/user_address.html',context)





@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
def add_new_address(request):

    if request.method == 'POST':
                # Form is not valid, handle the case when all fields are empty
        if request.POST['city'] == '' or request.POST['address'] == '' or request.POST['zip_code'] == '' or request.POST['country'] == '' :
            messages.error(request, 'Empty form cannot be submitted.')
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
            return render(request,'user_app/user_address.html',{'form':form})
        

    form = ShippingAddressForm()
  
    return render(request,'user_app/user_address.html',{'form':form})



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
@user_passes_test(is_user_authenticated, login_url='user:user_sign_in')
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

    
    #send_otp(otp)
    print('----------------------user account update otp---------------',request.session['otp'])
    if request.method == 'POST':

       #getting the otp
        entered_otp = f"{request.POST['otp1']}{request.POST['otp2']}{request.POST['otp3']}{request.POST['otp4']}"
        print(f"entered otp : {entered_otp} , user profile account update otp : {request.session['otp']}")
       
        if entered_otp == request.session['otp']:
            if 'user_account_resend_otp' in request.session:
                #delete only the resend otp value
                del request.session['user_account_resend_otp']
            if 'otp' in request.session:
                del request.session['otp']
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

