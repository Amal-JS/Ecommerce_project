from django.db import models
from user.models import CustomUser
from products.models import Variant


class Review(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE)
    star_rating = models.PositiveIntegerField(default=0)
    
    
    review = models.TextField()

    def __str__(self):
        return f"{self.user.username} {self.variant.name} : {self.id}"