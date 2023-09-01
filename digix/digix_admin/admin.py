from django.contrib import admin
from products.models import Product,Category,Variant,Variant_Images


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Variant)
admin.site.register(Variant_Images)
# Register your models here.
