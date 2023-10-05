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
    
    path('change_order_status/<int:id>/<str:value>/',views.change_order_status,name='change_order_status'),

    path('returns/',views.all_returns,name='returns'),

    path('return_order/<int:id>/',views.return_order,name='return_order'),

    path('return_reason_update/<str:order_num>/<int:variant_id>/<int:return_order_id>/',views.return_reason_update,name='return_reason_update'),

    path('accept_return_reason/<int:id>/',views.accept_return_reason,name='accept_return_reason'),

    #coupoun
    path('all_coupouns/',views.all_coupouns,name='all_coupouns'),

    path('add_coupoun/',views.add_coupoun,name='add_coupoun'),

    #get all variants,
    path('get_all_variants/',views.get_all_variants),
    path('edit_coupoun/<int:id>/',views.edit_coupoun,name='edit_coupoun'),

    #get all offers,
    path('all_offers/',views.all_offers,name='all_offers'),
    path('add_offer/',views.add_offer,name='add_offer'),
    path('edit_offer/<int:id>/',views.edit_offer,name='edit_offer'),

    path('change_offer_status/<int:id>/',views.change_offer_status,name='change_offer_status'),
    
    

]