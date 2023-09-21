from django.db import models
from products.models import Variant
from user.models import CustomUser


#Cart

class Cart(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variants')
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.variant.product.name+"---"+self.variant.ram+'----'+self.variant.storage+"---"+self.variant.color
