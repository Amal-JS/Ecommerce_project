from django.db import models

# Create your models here.

#category model
class Category(models.Model):
    name = models.CharField(max_length=30,unique=True)

    def __str__(self) -> str:
        return self.name
    
#brand model
class Brand(models.Model):
    name = models.CharField(max_length=30,unique=True)
    def __str__(self) -> str:
        return self.name

#product model
class Product(models.Model):
    name=models.CharField(max_length=30)
    category = models.ForeignKey(Category,related_name='category_products',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(Brand,related_name='brand_products',on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return self.name
    

class Variant(models.Model):

    tv_mount_choices = [
        ("wall mount","Wall Mount"),
        ("table mount","Table Mount")

    ]
    name = models.CharField(max_length=30,unique=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_variants')
    ram = models.PositiveBigIntegerField()
    storage = models.PositiveBigIntegerField()
    color = models.CharField(max_length=20)
    screen_resolution = models.DecimalField(max_digits=4,decimal_places=2)
    no_of_usb_ports = models.PositiveIntegerField(blank=True,null=True)
    no_of_hdmi_ports = models.PositiveIntegerField(blank=True,null=True)
    tv_mount = models.CharField(max_length=30,choices=tv_mount_choices,blank=True,null=True)

    def __str__(self) -> str:
        return f'{self.name} : {self.product}'
    

#image for a variant
class Variant_Images(models.Model):
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,related_name="variant_images")
    image=models.ImageField(upload_to='product_images/')
    def __str__(self) -> str:
        return self.variant

