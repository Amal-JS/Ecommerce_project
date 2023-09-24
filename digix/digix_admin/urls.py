from django.urls import path

from . import views
app_name= 'digix_admin'
urlpatterns = [
    path('',views.admin_home,name='admin_home'),

    path('admin_logout/',views.admin_logout,name='admin_logout'),

    path('admin_login/',views.admin_login,name='admin_login'),

    path('add_category/',views.add_category,name='add_category'),

    path('all_category/',views.all_category,name='all_category'),

    path('add_product/',views.add_product,name='add_product'),

    path('all_products/',views.all_products,name='all_products'),

    path('add_variant/',views.add_variant,name='add_variant'),

    path('all_variants/',views.all_variants,name='all_variants'),

    path('category_delete/<int:id>/',views.delete_category),

    path('category_update/<int:id>/',views.category_update),

    path('product_delete/<int:id>/',views.delete_product),

    path('product_update/<int:id>/',views.product_update),

    path('variant_delete/<int:id>/',views.delete_variant),

    path('variant_update/<int:id>/',views.variant_update),

    path('all_users/',views.all_users,name='all_users'),

    path('all_orders/',views.orders,name='orders'),
    
    path('change_order_status/<int:id>/<str:value>/',views.change_order_status,name='change_order_status')

    

]