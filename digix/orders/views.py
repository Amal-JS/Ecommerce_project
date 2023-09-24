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

#for printing pdf 
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

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
            # Retrieve all order details related to the order
            all_orders = OrderDetail.objects.filter(order=order)

            if all_orders:
                # Create a list to store variant and image information
                purchased_variants = []

                for order_detail in all_orders:
                    variant = order_detail.variant
                    variant_image = variant.variant_images.first()

                    # Access the associated address through the order object
                    address = order_detail.order.address  # Assuming 'address' is a ForeignKey in Order model

                    # Create a dictionary with variant, image, and address information
                    variant_info = {
                        'variant': variant,
                        'image': variant_image.image.url if variant_image else None,
                        'quantity': order_detail.quantity,
                        'total_price': order_detail.total_price,
                        'order_status': order_detail.order_status,
                        'is_returned': order_detail.is_returned,
                        'is_delivered': order_detail.is_delivered,
                        'delivered_date': order_detail.delivered_date,
                        # Add address details to the dictionary
                        'address': address.address,
                        'city': address.city,
                        'state': address.state,
                        'zipcode': address.zip_code,
                        
                        'country': address.country,
                    }

                    # Append the variant info to the list
                    purchased_variants.append(variant_info)

                return render(request, 'user_app/order_success.html', {'order': order, 'purchased_variants': purchased_variants})

    return redirect('user:user_cart')
     

#pdf generate on order
def generate_pdf(request, order_num):
    # Retrieve the order details based on the order_num
    order = Order.objects.filter(order_num=order_num).first()
    all_orders = OrderDetail.objects.filter(order=order)

    
    # Create an HttpResponse object with PDF content type and a suggested filename
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="order_{order.order_num}_{order.user.username}.pdf"'

    # Create a PDF object using the response as its "file."
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Create a list to hold the Story (elements that will be added to the PDF)
    Story = []

    # Define custom styles for the headings
    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    heading_style.alignment = 1  # Center alignment

    # Add the heading "Digix" as a big centered text
    Story.append(Paragraph("Digix", heading_style))
    Story.append(Spacer(1, 12))  # Add some space below the heading

    # Add the "Order Details" heading
    Story.append(Paragraph("Order Details", styles['Heading2']))
    Story.append(Spacer(1, 12))  # Add some space below the heading

    # Add user information
    user_info = [
        [Paragraph("Address", styles['Normal']), order.address.address],
        [Paragraph("City", styles['Normal']), order.address.city],
        [Paragraph("Zip Code", styles['Normal']), order.address.zip_code],
        [Paragraph("State", styles['Normal']), order.address.state],
        [Paragraph("Username", styles['Normal']), order.user.username],
        [Paragraph("Phone", styles['Normal']), order.user.phone],
    ]

    # Create a table for user information
    user_table = Table(user_info)
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
    ]))

    Story.append(user_table)
    Story.append(Spacer(1, 12))  # Add some space below the user information

    # Add the "Order Products" heading
    Story.append(Paragraph("Order Products", styles['Heading2']))
    Story.append(Spacer(1, 12))  # Add some space below the heading

    # Add order products information
    order_products_info = [
        [Paragraph("Variant", styles['Normal']), Paragraph("Quantity", styles['Normal'])],
    ]

    # Add each variant and its quantity to the table
    for order_detail in all_orders:
        order_products_info.append([order_detail.variant.product.name, str(order_detail.quantity)])

    # Create a table for order products
    order_products_table = Table(order_products_info)
    order_products_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
    ]))

    Story.append(order_products_table)
    Story.append(Spacer(1, 12))  # Add some space below the order products table

    # Add the total price of the order
    total_price_info = [
        [Paragraph("Total Price", styles['Normal']), f"Rs {order.total}"],
    ]

    # Create a table for the total price
    total_price_table = Table(total_price_info)
    total_price_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
    ]))

    Story.append(total_price_table)

    # Build the PDF document
    doc.build(Story)

    return response

    
   


def cancel_order(request, id):

    item = OrderDetail.objects.get(id=id)
    if item.order_status != 'cancelled' and item.order_status != 'delivered':
        item.order_status = 'cancelled'
        item.save()

    return redirect('user:user_profile_orders')


def return_order(request, id):
    item = OrderDetail.objects.get(id=id)
    if request.method == 'POST':
        item.order_status = 'returned'
        item.save()
        return redirect('user:user_profile_orders')

    if item.order_status == 'delivered':
        return render(request, 'pages/return_reason.html', {'item': item})