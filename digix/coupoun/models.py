from django.utils import timezone
from django.db import models
from user.models import CustomUser


class Coupons(models.Model):
    COUPOUN_TYPES =(
        ('general','General Coupoun'),
        ('category','Category Coupoun'),
        ('variant','Product Coupoun')
    )
    #coupoun name
    code = models.CharField(max_length=10)
    #discount in percentage
    discount_percentage = models.IntegerField()
    #cart_min_amount
    cart_min_amount = models.DecimalField(max_digits=10,decimal_places=2)
    #valid till
    valid_to = models.DateField()
    #active or not 
    is_active = models.BooleanField(default=True)
    #soft delete
    is_deleted = models.BooleanField(default=False)
    #coupoun type
    coupoun_type = models.CharField(max_length=20, choices=COUPOUN_TYPES)
    #if coupoun type is category or product we want to know to which we want to apply
    coupoun_applied_to = models.CharField(max_length=400,null=True,blank=True)
    #count of counpoun
    count = models.PositiveIntegerField()
    #if the cart amount is greater than this amount can't give the discount it will be so ,
    #for that giving an amount exactly to work for that 
    cart_max_amount = models.DecimalField(max_digits=10,decimal_places=2)
    #amount which want to be applied when max amount 
    discount_amount = models.DecimalField(max_digits=8,decimal_places=2)


    #check the coupoun is active or can be used
    @property
    def is_valid(self):
        now = timezone.now().date()
        return self.is_active and self.valid_to >= now

    def __str__(self):
        return self.code
    
    #methods to check if count is less than zero then make active and delte true
    def save(self, *args, **kwargs):
        if self.count <= 0:
            # If count is zero or negative, set is_active to False and is_deleted to True
            self.is_active = False
            self.is_deleted = True
        else:
            # If count is greater than zero, ensure is_active is True
            self.is_active = True
        
        super().save(*args, **kwargs)

    #by calling this method automatically the count is decreased and update the table
    def use_coupon(self):
        # Decrement the coupon count when it is used
        if self.count > 0:
            self.count -= 1
            self.save()


class UsedCoupons(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coupons = models.ForeignKey(Coupons, on_delete=models.CASCADE, related_name='user_coupons')

    class Meta:
        verbose_name_plural = 'Used Coupons'