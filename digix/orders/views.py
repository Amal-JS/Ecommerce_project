from django.http import JsonResponse
from django.shortcuts import redirect, render

#importing variant and custom user models , cart
from products.models import Variant
from user.models import CustomUser , ShippingAddress
from  . models import Cart , Order , OrderDetail ,UserPurchasedProducts
#import the function to check user authenticated

from  user.views import user_passes_test,is_user_authenticated

from django.db import transaction

from django.db.models import Sum


#order confirm

def order_confirm(request):
        
        user = request.user

        address_id = request.GET.get('selected_address',None)
        payment_method = request.GET.get('payment_method',None)

        if not address_id is None or payment_method is None:

            # Retrieve cart items for the user
            cart_items = Cart.objects.filter(user=user)

        
            with transaction.atomic():

                # Create the order 
                order = Order.objects.create(user=user)

                # Set the selected address if available
                if address_id:
                    
                        selected_address = ShippingAddress.objects.get(id=address_id)
                        order.address = selected_address
                        order.save()
                    

                # Process each product in the cart
                for cart_item in cart_items:
                    variant = cart_item.variant

                    # Create the order detail for the product
                    order_detail = OrderDetail.objects.create(
                        
                    order=order,  #order created above
                    variant=variant, #each variant in the cart
                    quantity=cart_item.quantity,  # quantity of each variant
                    total_price=variant.selling_price * cart_item.quantity  #total price for each variant with corresponding quantity
                )
                    

                    
                    # Check if the product already exists in the user's purchased list
                    existing_purchase = UserPurchasedProducts.objects.filter(user=user, variant=variant).first()

                    if existing_purchase:
                        # If the product exists, update the quantity by adding the current quantity
                        existing_purchase.quantity += cart_item.quantity
                        existing_purchase.save()
                    else:
                        # If the product doesn't exist, create a new entry in the purchased list
                        UserPurchasedProducts.objects.create(user=user, variant=variant, quantity=cart_item.quantity)


                    # Reduce the quantity in the variant stock
                    variant.stock -= cart_item.quantity
                    variant.save()

                    # Delete the product from the cart
                    cart_item.delete()

                # Calculate and set the total price for the order
                order_total_price = OrderDetail.objects.filter(order=order).aggregate(total=Sum('total_price'))
                order.total = order_total_price['total']

                

                order.payment_type = payment_method
                order.save()

                order_num = order.order_num
                return JsonResponse({'order_num':order_num},safe=False)

        return redirect('user:user_cart')

#order success page

def order_success(request,order_num=None):
     
    # order_num = request.GET.get('order_num',None)
    # print(order_num)
    if order_num:
        # Find the order with the given order_num
        order = Order.objects.filter(order_num=order_num).first()
        
        if order:
            return render(request, 'user_app/order_success.html', {'order': order})

    return redirect('user:user_cart')
     
   


# def cancel_order(request, id):

#     item = OrderDetail.objects.get(id=id)
#     if item.order_status != 'cancelled' and item.order_status != 'delivered':
#         item.order_status = 'cancelled'
#         item.save()

#     return redirect('profile_orders')


# def return_request(request, id):
#     item = OrderDetail.objects.get(id=id)
#     if request.method == 'POST':
#         item.order_status = 'returned'
#         item.save()
#         return redirect('profile_orders')

#     if item.order_status == 'delivered':
#         return render(request, 'pages/return_reason.html', {'item': item})