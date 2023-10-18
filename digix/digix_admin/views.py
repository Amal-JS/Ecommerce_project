#report generation
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet

from django.http import HttpResponse

from datetime import timedelta
from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from coupoun.models import Coupons
from coupoun.models import Offers
from orders.models import Wallet
from products.models import Variant_Images
from products.forms import CategoryForm,ProductForm,VariantForm
from django.contrib import messages
from products.models import Category,Product,Variant
from user.models import CustomUser
#for variant images and variant adding we are using 'transactions' in db
from django.db import transaction
from django.contrib.auth.models import User

#check user authentication , login and logout (adding and removing user in session )
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password, check_password
from django.utils.safestring import mark_safe

from django.contrib.auth.decorators import user_passes_test

#import Orders
from orders.models import OrderDetail,Order,ReturnOrder
from django.utils.text import capfirst
#import CoupounForm
from coupoun.forms import CoupounForm,OfferForm
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta, datetime, time

def is_user_authenticated(user):
    return user.is_authenticated and user.is_superuser


#admin home 
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def admin_home(request):
        #getting dates
        today = timezone.now().date()
        month = timezone.now().month
        current_date = timezone.now()
        
        daily_sales_count = OrderDetail.objects.filter(order_status='delivered',
                                                       order__date_created__date=today).aggregate(
            delivered_count=Count('order'))
        daily_sales_amount = OrderDetail.objects.filter(order_status='delivered',
                                                        order__date_created__date=today).aggregate(
            delivered_amount=Sum('total_price')) 
        # Count of daily Orders
        daily_orders_count = OrderDetail.objects.filter(delivered_date=today).aggregate(orders_count=Count('order'))
        print(OrderDetail.objects.filter(delivered_date=today))
        

        total_orders = Order.objects.all().count()
        total_users = CustomUser.objects.all().count()
        total_sales = OrderDetail.objects.filter(order_status = 'delivered').count()
        total_profit_result = OrderDetail.objects.filter(order_status='delivered').aggregate(Sum('total_price'))
        total_profit = total_profit_result['total_price__sum'] if total_profit_result['total_price__sum'] is not None else 0
        total_cancelled = OrderDetail.objects.filter(order_status = 'cancelled').count()
        total_returned = OrderDetail.objects.filter(order_status='returned').count()
        order_count_today = 0  if daily_orders_count['orders_count'] is None else daily_orders_count['orders_count']
        
        print(daily_sales_amount)

        context = {
            'total_users':total_users,
            'total_sales' : total_sales ,
            'total_profit' :total_profit, 
            'total_cancelled':total_cancelled,
            'total_returned':total_returned,
            'total_orders'      :total_orders,
            'daily_sales_count': daily_sales_count['delivered_count'],
            'daily_sales_amount': daily_sales_amount['delivered_amount'],
            'daily_orders_count':  order_count_today,
            
        }
        
        return render(request,'digix_admin/index.html',context)
#order data
def get_order_data(request):
    today = timezone.now()
    seven_days_ago = today - timedelta(days=6)

    orders_by_day = Order.objects.filter(
        date_created__range=(seven_days_ago, today)
    ).values('date_created__day').annotate(order_count=Count('id'))

    order_data = [0] * 7  # Initialize with zeros for all days of the week

    for order in orders_by_day:
        day = (order['date_created__day'] + 6) % 7  # Adjust for array indexing
        order_data[day] = order['order_count']

    return JsonResponse({'order_data': order_data})

#order count in returned , cancelled ,total and delivered
from django.http import JsonResponse

def chart_order_status(request):
    # Simulated data, replace with actual data retrieval logic
    orders_count = Order.objects.all().count()
    canceled_count = OrderDetail.objects.filter(order_status='cancelled').count()
    returned_count = OrderDetail.objects.filter(order_status='returned').count()
    delivered_count = OrderDetail.objects.filter(order_status='delivered').count()

    # Create a dictionary with the data
    chart_data = {
        "labels": ["Orders", "Canceled", "Returned", "Delivered"],
        "datasets": [
            {
                "data": [orders_count, canceled_count, returned_count, delivered_count],
                "backgroundColor": [
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56",
                    "#4BC0C0",
                ],
            }
        ],
    }

    return JsonResponse(chart_data)

#admin login
def admin_login(request):

    if request.method == "POST":
        admin_username = request.POST['admin_username']
        admin_password =request.POST['admin_password']
        #print(admin_username,admin_password)

        admin=authenticate(request,username=admin_username,password=admin_password)
        if admin:
            if admin.is_superuser:
                login(request,admin)
                return redirect('digix_admin:admin_home')
            else:
                messages.error(request,'invalid credentials')
                return redirect('digix_admin:admin_login')

        else:
            print(admin)
            messages.error(request,'invalid credentials')
            return redirect('digix_admin:admin_login')


        # try:
        #     admin=CustomUser.objects.get(username=admin_username)
        #     psd_hsd = CustomUser.make_password(admin,admin_password)

        #     #print(psd_hsd)

        #     if admin.password == psd_hsd and admin.is_superuser:
        #         login(request,admin)
        #         return redirect('digix_admin:admin_home')
            
        #     else:
        #         messages.error(request,'invalid credentials')
        #         return redirect('digix_admin:admin_login')
            
        # except Exception as e:
        #     messages.error(request,'invalid credentials')
        #     return redirect('digix_admin:admin_login')
        
    return render(request,'digix_admin/login.html')


#logout admin
def admin_logout(request):
    logout(request)

    return redirect('digix_admin:admin_login')

#check form fields which are empty and which are not and return True or false based on that
#required fields is a list which which are required
def is_form_empty(form, required_fields):
    # Check if all fields except required ones are empty
    return all(not value for field_name, value in form.cleaned_data.items() if field_name not in required_fields)

#add new category
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def add_category(request):

    if request.method == 'POST':

        
        form = CategoryForm(request.POST)

        # Define which fields are required
        required_fields = ['name']
        
        

        # Check if the required fields are filled in
        missing_fields = [field_name for field_name in required_fields if not request.POST.get(field_name)]

        if missing_fields:
            missing_fields_message = '<br>'.join(missing_fields)  # Join missing fields with <br>
            messages.warning(request, mark_safe(f"The following required fields are missing:<br>{missing_fields_message}"))
            return render(request, 'digix_admin/add_form.html', {'element': 'Category Form', 'form': form})

        if form.is_valid():

            form.save()
            return redirect('digix_admin:all_category')
            
        else:
            #if error show it in the page 
            messages.warning(request,form.errors)
            return render(request,'digix_admin/add_form.html',{'element':'Category Form','form':form})
    form = CategoryForm()
    return render(request,'digix_admin/add_form.html',{'form':form,'element':'Category'})

#add new product
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def add_product(request):


    if request.method == 'POST':

        
        form = ProductForm(request.POST)

        # Define which fields are required
        required_fields = ['name','category','brand']
        
        

        # Check if the required fields are filled in
        missing_fields = [field_name for field_name in required_fields if not request.POST.get(field_name)]

        if missing_fields:
            missing_fields_message = '<br>'.join(missing_fields)  # Join missing fields with <br>
            messages.warning(request, mark_safe(f"The following required fields are missing:<br>{missing_fields_message}"))
            return render(request, 'digix_admin/add_form.html', {'element': 'Product Form', 'form': form})



        if form.is_valid():
            form.save()
            return redirect('digix_admin:all_products')
        else:
            messages.warning(request,form.errors)
            
            return render(request,'digix_admin/add_form.html',{'form':form,'element':'Product'})
    form = ProductForm()
    return render(request,'digix_admin/add_form.html',{'form':form,'element':'Product'})


#addding new variant with images corresponding to the variant object
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def add_variant(request):
    if request.method == 'POST':
        form = VariantForm(request.POST)

        # Define which fields are required
        required_fields = ['name',
                           'product',
                           'ram',
                           'stock',
                           'storage',
                           'color',
                           'mr_price',
                           'selling_price',
                           'screen_resolution',


                           ]
        
        

        # Check if the required fields are filled in
        missing_fields = [field_name for field_name in required_fields if not request.POST.get(field_name)]

        if missing_fields:
            missing_fields_message = '<br>'.join(missing_fields)  # Join missing fields with <br>
            messages.warning(request, mark_safe(f"The following required fields are missing:<br>{missing_fields_message}"))
            return render(request,'digix_admin/add_form.html',{'form':form,'element':'Variant'}) 
        

        if form.is_valid():

            try:

                with transaction.atomic():
                    
                    #variant object is saved only if the five image field is accepted image field can be empty
                    variant=form.save()

                    #passing each image to Variant Image model
                    #five image field
                           
                            
                    for i in range(1, 6):
                        #getting each image from request.FILES
                        uploaded_file = request.FILES.get(f'image{i}')
                        if uploaded_file:
                            try:
                                variant_image = Variant_Images(variant=variant, image=uploaded_file)
                                variant_image.full_clean()  # Validate the uploaded file 
                                variant_image.save()

                            except ValidationError as e:
                                #error occur while accepting image
                                messages.error(request, e)

                    return redirect('digix_admin:all_variants')
                

            except Exception as e:
                #error occuring in transaction
                messages.error(request,e)
                return render(request,'digix_admin/add_form.html',{'form':form,'element':'Variant'})      

            
            
        else:
            messages.warning(request,form.errors)
            
            return render(request,'digix_admin/add_form.html',{'form':form,'element':'Variant'})
    
    #new form send wile accessing the page using get request
    form = VariantForm()
    return render(request,'digix_admin/add_form.html',{'form':form,'element':'Variant'})



#get all categories
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def all_category(request):
    categories = Category.objects.all()
    
    
    return render(request,'digix_admin/category.html',{'categories':categories})

#get all products
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def all_products(request):
    products = Product.objects.all()
    return render(request,'digix_admin/product.html',{'products':products})

#get all variants
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def all_variants(request):
    variants = Variant.objects.all()
    return render(request,'digix_admin/variant.html',{'variants':variants})

#get all users
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def all_users(request):
    users = CustomUser.objects.all()
    return render(request,'digix_admin/users.html',{'users':users})    

   
def  delete_category(request,id):
    cat_obj= Category.objects.get(id=id)
    cat_obj.delete()
    return redirect("digix_admin:all_category")


def  delete_product(request,id):
    cat_obj= Product.objects.get(id=id)
    cat_obj.delete()
    return redirect("digix_admin:all_products")


def  delete_variant(request,id):
    cat_obj=Variant.objects.get(id=id)
    cat_obj.delete()
    return redirect("digix_admin:all_variants")


#update category object
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def category_update(request, id):
    #will raise exception if object not found
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        #passing the new form values with existing instance
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('digix_admin:all_category')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'digix_admin/add_form.html', {'form': form, 'element': category,'update':True})


@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def product_update(request, id):
    
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('digix_admin:all_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'digix_admin/add_form.html', {'form': form, 'element': product,'update':True})

# Retrieve the Variant instance to be updated using its primary key (id)
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def variant_update(request, id):
    variant = Variant.objects.get(pk=id)

    if request.method == 'POST':
        # Create a VariantForm instance with the data from the request, including uploaded files, and bind it to the existing Variant instance
        form = VariantForm(request.POST, request.FILES, instance=variant)
        if form.is_valid():
            # Check if new images have been uploaded
            new_images = []

            # Loop through image fields (image1, image2, ..., image5)
            for i in range(1, 6):
                image_field_name = f'image{i}'
                try:
                    # Attempt to retrieve an uploaded image from request.FILES
                    image = request.FILES.get(image_field_name, None)
                    if image:
                        new_images.append(image)
                except ValidationError as e:
                    # If there's a validation error (unlikely in this context), show an error message and return to the form
                    messages.error(request, e)
                    return render(request, 'digix_admin/add_form.html', {'form': form, 'element': 'Variant', 'update': True})

            if new_images:
                # Delete existing images associated with the variant
                variant.variant_images.all().delete()

                # Create new Variant_Images instances for the variant with the new images
                for image in new_images:
                    Variant_Images.objects.create(variant=variant, image=image)

            # Save the updated variant with or without new images
            form.save()
            return redirect('digix_admin:all_variants')
        else:
            # If the form is not valid, display form errors and return to the form
            messages.error(request, form.errors)
            return render(request, 'digix_admin/add_form.html', {'form': form, 'element': 'Variant', 'update': True})

    else:
        # If it's a GET request, create a VariantForm instance pre-filled with the existing variant data
        form = VariantForm(instance=variant)

    # Render the form page for updating the variant
    return render(request, 'digix_admin/add_form.html', {'form': form, 'element': 'Variant', 'update': True})


#admin orders page
@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def orders(request):
    # Use select_related() to fetch related Order and User data
    all_orders = OrderDetail.objects.select_related('order__user').order_by('-order__date_created').all()

    # Use prefetch_related() to fetch related Variant data
    all_orders = all_orders.prefetch_related('variant')

    # Create a list to store modified order objects for rendering
    orders = []

    # Loop through the orders and update order_status for rendering
    for order in all_orders:
        # Transform the order_status value and create a copy of the order detail
        modified_order = order
        modified_order.order_status = capfirst(order.order_status.replace('_', ' '))
        orders.append(modified_order)

    # Count the number of orders
    count = all_orders.count()

    return render(request, 'digix_admin/admin_orders.html', {'orders': orders, 'count': count})


#admin orders page

def change_order_status(request, id, value):
    try:
        order = OrderDetail.objects.get(id=id)
        order.order_status = value
        
        if order.order_status == 'shipped':
            order.delivered_date= order.order.date_created + timedelta(days=7)
        print('order delivered date ',order.delivered_date,'order.order.date_created + timedelta(days=7)  ',order.order.date_created + timedelta(days=7))
        if order.order_status == 'delivered':
            order.delivered_date= datetime.now()
        order.save()
        print(order,order.delivered_date)
        return JsonResponse({'order_status_changed': True, 'new_status': value})
    except Exception as e:
        return JsonResponse({'order_status_changed': False, 'response_error': str(e)})
    

@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def all_returns(request):
    return_orders = ReturnOrder.objects.all()
    return render(request,'digix_admin/Returns.html',{'return_orders':return_orders})


@user_passes_test(is_user_authenticated, login_url='digix_admin:admin_login')
def return_order(request,id):
    return_order =ReturnOrder.objects.get(id=id)
    return render(request,'digix_admin/return_order.html',{'return_order':return_order})


#admin update after reading the return reason 
def return_reason_update(request,order_num,variant_id,return_order_id):

    variant=Variant.objects.get(id=variant_id)
    order = Order.objects.get(order_num=order_num)
    item = OrderDetail.objects.filter(order=order,variant=variant).first()
    return_order =ReturnOrder.objects.get(id=return_order_id)
    #order detail item
    if request.method == 'POST':
        
        if request.POST['reason'] == '':
            
            return render(request,'digix_admin/return_order.html',{'return_order':return_order,'msg':'Cannot validate empty form'})

        item.return_approved = False
        item.order_status = 'shipped'
        item.return_admin_response = request.POST['reason'] 
        print(f"request.POST['reason']  : {request.POST['reason'] } , item : {item.return_admin_response}")
        item.save()

    return redirect('digix_admin:return_order',id=return_order_id)

#if return reason can be accepted  , return order id 
def accept_return_reason(request,id):
    return_order =ReturnOrder.objects.get(id=id)
    order_detail = return_order.order
    user= order_detail.order.user
    variant = Variant.objects.get(id=order_detail.variant.id)

    return_order.admin_approved = True #Admin approved
    return_order.payment_returned = True #payment returned
    return_order.qty_updated  = True #quantity updated
    return_order.recieved  = True #recieved

    order_detail.order_status = 'returned' #order status changed
    print('order_detail.variant.stock',variant.stock)
    #stock update
    print('variant.stock += order_detail.quantity',variant.stock,order_detail.quantity,'order staus', order_detail.order_status)
    variant.stock += order_detail.quantity
    variant.save()
    print('order_detail.variant.stock update',variant.stock)
    #making the admin response 
    order_detail.return_admin_response = 'Request Accepted'
    order_detail.return_approved = True

    #Wallet amount update
    user_wallet = Wallet.objects.filter(user=order_detail.order.user).first()
    
    user_wallet.amount += order_detail.total_price
    
    user_wallet.save()
    order_detail.save()
    return_order.payment_initiated_date =datetime.now()
    return_order.save()
    

    return redirect('digix_admin:return_order',id=id)



#coupoun

def all_coupouns(request):
    coupouns = Coupons.objects.all()
    context=''
    return render(request,'digix_admin/coupoun.html',{'coupouns':coupouns})

# get all variants 
def get_all_variants(request):
    # Get all variants and extract their names
    all_variants = Variant.objects.all()
    variant_names = [variant.name for variant in all_variants]

    # Create a JSON response with the variant names
    response_data = {
        'variants': variant_names
    }
    print(variant_names)
    return JsonResponse(response_data)


def add_coupoun(request):

    if request.method == 'POST':
        # Check if all fields are empty
        # Check if any field in the form is empty
        if any(not value for value in request.POST.values()):
            messages.error(request, 'Please fill  all fields.')
        else:
            form = CoupounForm(request.POST)
            if form.is_valid():
                # If the form is valid, process the data here
                # For example, save the coupon data to the database
                form.save()
                messages.success(request, 'Coupon added successfully!')
                return redirect('digix_admin:all_coupouns')  # Redirect to a success page
            else:
                messages.error(request, 'Error: Please fill in all required fields.')
    
    form = CoupounForm()

    context = {
        'form_what': 'Coupoun',
        'form': form
    }
    return render(request, 'digix_admin/add_coupoun_offer.html', context)



def edit_coupoun(request,id):
    coupoun = Coupons.objects.get(id=id)
    
    if request.method == 'POST':
        form = CoupounForm(request.POST,instance=coupoun)
        if form.is_valid():
                # If the form is valid, process the data here
                # For example, save the coupon data to the database
                form.save()
                messages.success(request, 'Coupon updated successfully!')
                return redirect('digix_admin:all_coupouns')  # Redirect to a success page
        else:
                messages.error(request,form.errors)

    form = CoupounForm(instance=coupoun)
    context = {
        'form_what': 'Coupoun',
        'form': form
    }
    return render(request, 'digix_admin/add_coupoun_offer.html', context)



#offers 
def all_offers(request):
    offers = Offers.objects.all().order_by('-created_at')
    return render(request,'digix_admin/offers.html',{'offers':offers})


def add_offer(request):

    if request.method == 'POST':
        # Check if all fields are empty
        # Check if any field in the form is empty
        if any(not value for field, value in request.POST.items() if field != 'variant'):
            messages.error(request, 'Please fill  all fields.')
        else:
            form = OfferForm(request.POST)
            if form.is_valid():
                try:
                        # Attempt to save the form data
                        form.save()
                        messages.success(request, 'Offer updated successfully!')
                        return redirect('digix_admin:all_offers')
                except ValidationError as e:
                        # Handle the validation error
                        form.add_error(None, e)  # Add the error to the form's non-field errors
                        messages.error(request, 'Validation error: ' + str(e))
            else:
                messages.error(request, 'Error: Please fill in all required fields.')
    
    form = OfferForm()

    context = {
        'form_what': 'Offer',
        'form': form
    }
    return render(request, 'digix_admin/add_coupoun_offer.html', context)

def edit_offer(request,id):

    offer = Offers.objects.get(id=id)
    

    if request.method == 'POST':
        form = OfferForm(request.POST,instance=offer)
        if form.is_valid():
                try:
                        # Attempt to save the form data
                        form.save()
                        messages.success(request, 'Offer updated successfully!')
                        return redirect('digix_admin:all_offers')
                except ValidationError as e:
                        # Handle the validation error
                        form.add_error(None, e)  # Add the error to the form's non-field errors
                        messages.error(request, 'Validation error: ' + str(e))
        else:
                messages.error(request,form.errors)

    
    form = OfferForm(instance=offer)
    
    context = {
        'form_what': 'Offer',
        'form': form
    }
    return render(request, 'digix_admin/add_coupoun_offer.html', context)

def change_offer_status(request,id):
    offer = Offers.objects.get(id=id)

    if offer.is_active:
        
            offer.is_active = False
            
            # Check if the 'is_valid' property has changed to False
            
            print(offer.is_valid,offer.variant)
            if  offer.is_valid:
                
                if offer.variant is not None:
                    print('deactivate offer variant')
                    print(f"offer variant =--------{offer.variant}----nospace")
                    # Check if there is an active category offer for this variant

                    category_offer = Offers.objects.filter(category=offer.category, is_active=True,variant__isnull=True).exclude(id=offer.id).first()
                    if category_offer:
                        print('category offer for the variant available :',category_offer.name)
                        # Set the variant's selling price to the category offer price
                        offer.variant.selling_price = int(offer.variant.price_before_offer -  (offer.variant.price_before_offer * (category_offer.discount_percentage / 100)))
                        offer.variant.save()
                    else:
                        # Set the variant's selling price to the price before the offer
                        print('category offer for the variant  not available :',offer.variant.selling_price)
                        offer.variant.selling_price = offer.variant.price_before_offer
                        offer.variant.save()
                        print('category offer for the variant  not available after saving:',offer.variant.selling_price)
                    

                elif offer.category:
                    print('deactivate category :')
                    # Find all variants in the category and set their selling prices
                    variants_in_category = Variant.objects.filter(product__category=offer.category)
                    for variant in variants_in_category:
                        # print(variant.name,'-------- before updating price ------------',variant.selling_price)
                        # Check if the variant has an existing offer
                        existing_variant_offer = Offers.objects.filter(variant=variant, is_active=True).first()
                        if not existing_variant_offer:
                            # Set the variant's selling price to the price before the offer
                            variant.selling_price = variant.price_before_offer
                            # print(variant.name,'-------- after updating price ------------',variant.selling_price)
                            
                        else:
                            variant.selling_price = int(variant.price_before_offer - (variant.price_before_offer * (existing_variant_offer.discount_percentage / 100)))
                        #     print(variant.name,'-------- after updating price ------------',variant.selling_price)
                        variant.save()
            offer.save()
        
    else:
        #activating offer
        if offer.is_valid:
            
            
            
            if offer.variant is not None:
                # Set the 'is_active' field to False when creating a new offer
                
                print(' updating starting phase True case')
                # Check if an offer already exists for this variant
                existing_variant_offer = Offers.objects.filter(variant=offer.variant, is_active=True).exclude(id=offer.id).first()
                
                if existing_variant_offer:
                    # An active offer for this variant already exists
                    messages.error(request,f"An active offer already exists for the variant {offer.variant.name}")
                    return redirect('digix_admin:all_offers')
                
                offer.is_active = True
                # Check if the offer is valid
                if offer.is_valid:
                    # Set the variant's selling price to the new offer price
                    print('offer.variant.price_before_offer',offer.variant.price_before_offer,'offer.variant.selling_price',offer.variant.selling_price)

                    if offer.variant.price_before_offer > 0 and offer.variant.price_before_offer > offer.variant.selling_price:
                        print('in if block')
                        
                        offer.variant.selling_price = int(offer.variant.price_before_offer - (offer.variant.price_before_offer * (offer.discount_percentage / 100)))
                        offer.variant.save()
                    else:
                        print('came in else block')
                        offer.variant.price_before_offer = offer.variant.selling_price
                        offer.variant.selling_price = int(offer.variant.price_before_offer - (offer.variant.price_before_offer * (offer.discount_percentage / 100)))
                        offer.variant.save()
                    
            else:
                # Check if there is an existing valid offer for this category
                existing_category_offers = Offers.objects.filter(category=offer.category, is_active=True).exclude(id=offer.id)
               
                # Check if there are variant offers for products in this category
                variants_in_category = Variant.objects.filter(product__category=offer.category)
                existing_variant_offers = Offers.objects.filter(variant__in=variants_in_category, is_active=True).exclude(id=offer.id)
                


              
                # Remove the offer objects in existing_variant_offers if they exist in existing_category_offers
                existing_category_offers = existing_category_offers.exclude(variant__in=existing_variant_offers.values_list('variant', flat=True))
                


                


                if existing_category_offers.exists():
                    # Active offers for this category (including current category offer) or variant offers in this category exist
                    messages.error(request,f"An active offer already exists for the category {offer.name}")
                    return redirect('digix_admin:all_offers')
                
                offer.is_active = True
                # Check if this offer is valid
                if offer.is_valid:
                    # Get all variants in the category
                    variants_in_category = Variant.objects.filter(product__category=offer.category)
                    
                    for variant in variants_in_category:
                        # Check if the variant has an existing offer
                        existing_variant_offer = Offers.objects.filter(variant=variant, is_active=True).first()

                        if existing_variant_offer:
                            # Skip this variant if it already has an offer
                            continue

                        variant.price_before_offer = variant.selling_price
                        # Update the variant's selling price and price_before_offer
                        variant.selling_price = int(variant.price_before_offer - (variant.price_before_offer * (offer.discount_percentage / 100)))
                        variant.save()
            
            offer.save()
        else:
            messages.error(request,'Date is not in the time period')

    return redirect('digix_admin:all_offers')


#----------------------------------------------- order report -------------------------------------



def create_title(title_text):
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    return Paragraph(title_text, style=title_style)


def create_table(data, style):
    table = Table(data, style=style)
    return table


def create_pdf_response(report_type, elements):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={report_type}_report.pdf'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def generate_pdf_report(sales_data, total_canceled_sales, total_price_for_orders, total_orders_count, report_type):
    elements = []

    # Create Title
    title_text = f"Digix {report_type.capitalize()} Report"
    elements.append(create_title(title_text))
    elements.append(Spacer(1, 12))
    # Create Table for Data
    table_data = [["Product Name (Variant)", "Total Quantity", "Total Price"]]

    for order_detail in sales_data:
        product_name = f"{order_detail['variant__product__name']} (RAM: {order_detail['variant__ram']}GB, Storage: {order_detail['variant__storage']}GB)"
        variant_name = f"{order_detail['variant__product__name']} (RAM: {order_detail['variant__ram']}GB, Storage: {order_detail['variant__storage']}GB)"
        quantity = str(order_detail['total_quantity'])
        total_price = f"Rs {order_detail['total_price']}"  # Format the total price as 'Rs X'
        table_data.append([product_name,  quantity, total_price])

    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), (0, 0, 0)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
    ]

    elements.append(create_table(table_data, table_style))
    # Create a spacer to add some space between the table and the total info paragraph
    elements.append(Spacer(1, 20))

    total_info = f"Total Canceled {report_type.capitalize()}: {total_canceled_sales}<br/><br/><br/>"
    total_info += f"Total  {report_type.capitalize()}: {total_orders_count}<br/><br/><br/>"
    total_info += f"Total Profit: Rs {int(total_price_for_orders)}\n"  # Use the calculated total_price_for_orders
    

    # Add total_info as a Paragraph to elements
    total_info_paragraph = Paragraph(total_info, style=getSampleStyleSheet()['Normal'])
    elements.append(total_info_paragraph)

    return create_pdf_response(report_type, elements)

def download_report(request):

    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    month = request.GET.get('month', None)
    year = request.GET.get('year', None)
    report_type = 'orders'


    if (not start_date and not end_date) or (not month and not year) or not report_type:
        # Handle missing or invalid parameters
        messages.error(request,"Invalid parameters")
        return redirect('digix_admin:admin_home')
    
    if month != 'Select Month':
        if month and year:
            # If month and year are provided, calculate the start and end dates accordingly
            month = int(month)
            year = int(year)
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1) 
    
    
    


    # Calculate total orders, canceled orders, and total price within the specified date range
    order_data = OrderDetail.objects.filter(
        order__date_created__range=(start_date, end_date)
    ).values(
    'variant__name',  # Include the variant name
    'variant__product__name',  # Include the product name
    'variant__ram',  # Include the variant RAM
    'variant__storage',  # Include the variant storage
    ).annotate(
    total_quantity=Sum('quantity'),
    total_price=Sum('total_price')  # Calculate the total price for orders
    ).order_by('-total_quantity')

    total_canceled_orders = OrderDetail.objects.filter(
        order_status='cancelled',
        order__date_created__range=(start_date, end_date)
    ).count()

    total_orders_count = OrderDetail.objects.filter(
        order__date_created__range=(start_date, end_date)
    ).count()
    
    # Calculate total price for orders within the date range
    total_price_for_orders = int(sum(order['total_price'] for order in order_data))
    
    # Call generate_pdf_report with the correct arguments for "orders" report
    return generate_pdf_report(order_data, total_canceled_orders, total_price_for_orders, total_orders_count, report_type)
