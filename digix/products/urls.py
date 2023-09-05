from django.urls import path

from . import views

app_name='product'

urlpatterns=[
path('category/',views.get_all_category,name='all_category'),
path('product/',views.get_all_products,name='all_products'),
path('variant/',views.get_all_variants,name='all_variants'),
path('variant_with_image/',views.get_variant_data,name="variant_with_image")


]