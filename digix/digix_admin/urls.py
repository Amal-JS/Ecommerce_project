from django.urls import path
from . import views
app_name= 'digix_admin'
urlpatterns = [
    path('',views.admin_home,name='admin_home'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('add_category/',views.add_category,name='add_category'),
    path('all_category/',views.all_category,name='all_category'),
    path('add_product/',views.add_product,name='add_product'),
    path('all_products/',views.all_products,name='all_products'),
    path('add_variant/',views.add_variant,name='add_variant'),
    path('all_variants/',views.all_variants,name='all_variants')
]