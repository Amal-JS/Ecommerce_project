from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib
# Create your models here.


#custom user model with phone field

class CustomUser(AbstractUser):

    phone = models.CharField(max_length=10)


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
    def make_password(self, raw_password):
        
        #hashing logic
        
        salt = 'abcdefghijk'  # Add a unique salt value

        hashed_password = hashlib.sha256((salt + raw_password).encode()).hexdigest()
        return hashed_password
    
#checking password when loging 
#the input password will be hashed and checked with the user object password hashed value

    def check_password(self, raw_password):
        hashed_input_password = self.make_password(raw_password)
        return self.password == hashed_input_password
    
    
    

''' 
After this now we have to set in settings that our CustomUser want to be used as
the User model in our django project . So now go to settings.py and add
AUTH_USER_MODEL = 'user.CustomUser'

'''