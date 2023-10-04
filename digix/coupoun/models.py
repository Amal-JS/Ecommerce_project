from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from products.models import Category,Variant
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


#offfer


class Offers(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='offers')
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percentage = models.DecimalField(max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Offers'

    def __str__(self):
        return self.name

    @property
    def is_valid(self):
        now = timezone.now().date()
        print('start date',self.start_date,' now',now,  'end_date :',self.end_date)
        return self.start_date <= now <= self.end_date
    

    


    def save(self, *args, **kwargs):
        if self.discount_percentage > 40 :
            raise ValidationError(f"Offer percent cannot excced 40%.")
        
        if not self.id:

            if self.variant:
                
                # Check if an offer already exists for this variant
                existing_variant_offer = Offers.objects.filter(variant=self.variant, is_active=True).first()

                if existing_variant_offer:
                    # An active offer for this variant already exists
                    print('variant error')
                    raise ValidationError(f"An active offer already exists for the variant {self.variant.name}")

               
            else:
                # Check if there is an existing valid offer for this category
                existing_offer = Offers.objects.filter(category=self.category, is_active=True).exclude(id=self.id).first()
                if existing_offer:
                    # An active offer for this category already exists
                    raise ValidationError(f"An active offer already exists for the category {self.category.name}")

    
        super().save(*args, **kwargs)