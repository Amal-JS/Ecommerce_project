from django.db import models
import random


#function to generate a random number for each object
#because for security reasons we can't display the orginal id of product or variant or category
def generate_random_8_digit_number():
    # Generate an 8-digit random number
    min_value = 10000000  # Smallest 8-digit number
    max_value = 99999999  # Largest 8-digit number
    return random.randint(min_value, max_value)



#category model
class Category(models.Model):

    name = models.CharField(max_length=30,unique=True)
    rand_id = models.BigIntegerField(default=generate_random_8_digit_number,unique=True)
    is_availble = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    


#product model
class Product(models.Model):

    name=models.CharField(max_length=30,unique=True)
    category = models.ForeignKey(Category,related_name='category_products',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    brand = models.CharField(max_length=30)
    rand_id = models.BigIntegerField(default=generate_random_8_digit_number,unique=True)

    def __str__(self) -> str:
        return self.name
    

class Variant(models.Model):

    tv_mount_choices = [
    (' ', ' '),  # Empty or default choice
    ("wall mount", "Wall Mount"),
    ("table mount", "Table Mount")
]

    name = models.CharField(max_length=200,unique=True)
    rand_id = models.BigIntegerField(default=generate_random_8_digit_number,unique=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_variants')
    ram = models.PositiveIntegerField()
    storage = models.PositiveIntegerField()
    color = models.CharField(max_length=20)

    mr_price = models.DecimalField(max_digits=8,decimal_places=2)
    selling_price = models.DecimalField(max_digits=8,decimal_places=2)
    #when adding the offer to variant that offer price will be in the selling_price and the
    #amount on the selling_price will be on the price_before_offer
    #when offer ends the selling_price will be set to the previous price
    price_before_offer = models.DecimalField(max_digits=8,decimal_places=2,default=0)

    stock = models.PositiveIntegerField()
    is_available= models.BooleanField(default=False)
    screen_resolution = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)

    no_of_usb_ports = models.PositiveIntegerField(blank=True,null=True)
    no_of_hdmi_ports = models.PositiveIntegerField(blank=True,null=True)
    tv_mount = models.CharField(max_length=30,blank=True,null=True)
    
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} {self.name}'
       
    def save(self, *args, **kwargs):
        # Log the variant name and selling price before saving
        print(f"Saving variant: {self.name}, Selling Price: {self.selling_price}")
        
        # Call the parent class's save method to perform the actual save operation
        super(Variant, self).save(*args, **kwargs)

#image for a variant
class Variant_Images(models.Model):
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,related_name="variant_images")
    image=models.ImageField(upload_to='product_images/',null=True,blank=True)
    def __str__(self) -> str:
        return self.variant
    