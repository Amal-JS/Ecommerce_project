# for getting random numbers
import random
#for getting alaphabetic characters
import string

from django.db import models

#importing varaint , user and shipping address model
from products.models import Variant
from user.models import CustomUser,ShippingAddress


#Cart

class Cart(models.Model):

    #which user , helps on filtering purpose
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    #which variant
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variants')
    #how many variants selected ? default =1

    quantity = models.PositiveIntegerField(default=1)

    #on the checkout page there we need the total price of the product * quantity
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field for the total

    def calculate_total(self):
        return self.quantity * self.variant.selling_price
    
    #function which calcultes the total price with a helper function and saves it
    def save(self, *args, **kwargs):
        self.total = self.calculate_total()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.variant.product.name}---{self.variant.ram}----{self.variant.storage}---{self.variant.color}"




#order
class Order(models.Model):

    #payment choices 
    PAYMENT_CHOICES = (
        ('cash_on_delivery', 'Cash_on_Delivery'),
        ('online_payment', 'Online_payment'),
    )

    #function for generating the order id
    def generate_order_id():

                # A - Z         and            0 - 9
        chars = string.ascii_uppercase + string.digits
                # chars contain a string which has all uppercase characters and full digits

        return ''.join(random.choice(chars) for _ in range(10))

    #which user
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #which address
    address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    #date order created , automatically created
    date_created = models.DateTimeField(auto_now=True)
    #order num automatically genertated by the function
    order_num = models.CharField(max_length=20, default=generate_order_id)
    #type of payment given in choice 
    payment_type = models.CharField(max_length=100, choices=PAYMENT_CHOICES, default="Cash on delivery")
    #total price for the products in the single order
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username+"---"+self.order_num


#order detail model
#for each product in cart each order detail will be created with the same order id

class OrderDetail(models.Model):

    #order status
    ORDER_STATUS_CHOICES = (
        ('order_pending', 'Order_Pending'),
        ('order_confirmed', 'Order_Confirmed'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
        ('waiting_for_approval','Waiting_For_Approval'),
        ('returned', 'Returned'),
    )

    #order instance
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    #which variant / product
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    #quantity of the variant in the cart
    quantity = models.IntegerField(default=1)
    #total price for the variant , with quantity * price
    total_price = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    #status of order when creating an order will be order pending
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='order_pending')
    #when returning the product the variable be true
    return_approved = models.BooleanField(default=False)
    #whether admin reject return reason updated field
    return_admin_response = models.CharField(max_length=300,null=True)
    #date which will be added when product is delivered , default null
    delivered_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.order.user.username+"---"+self.variant.product.name+"---"+self.order_status



# user purchased products

class UserPurchasedProducts(models.Model):

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    #which variant
    variant = models.ForeignKey(Variant,on_delete=models.SET_NULL,null=True)
    #get the quantity
    quantity = models.PositiveIntegerField()




    def __str__(self):
        return f" { self.user.username} -- {self.variant.product.name} -- Quantity :{self.quantity}"




#Return products info storing model
class ReturnOrder(models.Model):

    order = models.ForeignKey(OrderDetail,on_delete=models.CASCADE,related_name='return_orders')
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    order_request_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=300)
    admin_approved = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    qty_updated = models.BooleanField(default=False)
    payment_returned = models.BooleanField(default=False)
    payment_initiated_date = models.DateTimeField(null=True,blank=True)
    

    def __str__(self) -> str:
        return f"{self.order.order.user.username} {self.order.order.order_num}, {self.variant.name}"

#wallet of user
class Wallet(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_wallet')
    amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self) -> str:
        return f"{self.user.username} : balance => {self.amount}"

#Damaged Products
class DamagedProducts(models.Model):
    
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,related_name='damaged_products')
    qty = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f" {self.variant.name}  Qty : {self.qty}"
#wallet usage
class WalletUsage(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name='user_wallet_usage')
    amount = models.DecimalField(max_digits=10,decimal_places=2) 
    order_num = models.ForeignKey(Order,on_delete=models.CASCADE)   
    date_used = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} {self.amount} {self.order_num}"


