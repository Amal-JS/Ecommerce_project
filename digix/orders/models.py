from django.db import models
from products.models import Variant
from user.models import CustomUser


#Cart

class Cart(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variants')
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
        return self.variant.product.name+"---"+self.variant.ram+'----'+self.variant.storage+"---"+self.variant.color
