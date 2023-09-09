from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


#custom user model with phone field

class CustomUser(AbstractUser):

    phone = models.IntegerField()


    # Add related_name arguments to avoid reverse accessor clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
    )

    def __str__(self):
        return self.username
    
    
    

''' 
After this now we have to set in settings that our CustomUser want to be used as
the User model in our django project . So now go to settings.py and add
AUTH_USER_MODEL = 'user.CustomUser'

'''