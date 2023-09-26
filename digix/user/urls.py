from django.urls import path
from . import views

#order views
from orders.views import order_confirm,order_success,return_order,cancel_order,generate_pdf
#review views 
from review.views import add_review,delete_review,update_review



app_name='user'

urlpatterns =[

#home page
path('',views.index,name='index'),

#get all products
path('all_products/',views.category_display_all_products,name='all_products'),
#get products on category or brand name
  path('all_products/<str:category>/', views.category_display_all_products, name='category_display_all_products'),
    #get products on category or brand name on filter value
    path('all_products/<str:category>/<str:sort_option>/', views.category_display_all_products, name='category_display_all_products'),
    #path('all_products/<str:category>/<str:brand>/<str:sort_option>/', views.category_display_all_products, name='category_display_all_products'),


#get specafic product
path('product/<int:id>/',views.product,name="product"),

#get variants for a particular product
path('product/simillar_variants/<int:id>/',views.get_variants),

#user login , sign up , logout

path('user_sign_in/',views.user_sign_in,name='user_sign_in'),


path('user_sign_up/',views.user_sign_up,name='user_sign_up'),
path('user_logout/',views.user_logout,name='user_logout'),


#user sign up , fetch , dyanmic field value checking
path('user_sign_up_value/',views.user_sign_up_value,name='user_sign_up_value'),

#search results
path('search_results/',views.search,name='search'),

#search json
 path('search_variants/', views.search_variants, name='search_variants'),

#get all users
path('user/get_all_users/',views.get_all_users),
path('user/unblock/<int:id>/',views.user_unblock),
path('user/block/<int:id>/',views.user_block),

#forgot password
path('forgot_password/',views.forgot_password,name='forgot_password'),
#verify otp
path('verify_otp/',views.verify_otp,name='verify_otp'),

#user password update
path('user_password_update/<int:id>/',views.user_password_update,name='user_password_update'),

#otp resend , update
path('otp_update/',views.otp_update,name='otp_update'),



#profile page
path('profile/',views.user_profile,name='user_profile'),



#wishlist page
path('wishlist/',views.user_wishlist,name='user_wishlist'),

#checkout page
path('checkout/',views.user_checkout,name='user_checkout'),


#user profile views
path('dashboard/',views.user_profile_dashboard,name='user_profile_dashboard'),
path('orders/',views.user_profile_order,name='user_profile_orders'),
path('address/',views.user_profile_address,name='user_profile_address'),

#view handle update user details except password update
path('account_details',views.user_profile_account_details,name='user_profile_account_details'),

#update password
path('profile_password_update/',views.user_profile_password_update,name='user_profile_password_update'),

#password change validating form
 path('account_password_update/', views.user_account_password_update, name='user_account_password_update'),

#user sign up , fetch , dyanmic field value checking
path('user_account_details_update_value/',views.user_account_details_update_value,name='user_account_details_update_value'),


#add new address 
path('add_new_address/',views.add_new_address,name='add_new_address'),
#update address
path('update_address/<int:id>/',views.update_address,name='update_address'),
#delete address
path('delete_address/<int:id>/',views.delete_address,name='delete_address'),
#set default address
path('default_address/<int:id>/',views.default_address,name='default_address'),

#checking user authenticated , already in wishlist  and already in cart
path('user_logged_in_status/',views.user_logged_in_status),
path('variant_in_wishlist_status/',views.variant_in_wishlist_status),

#product adding in wish list
path('add_to_wishlist/<int:id>/',views.add_to_wishlist,name='add_to_wishlist'),
#remove product from wishlist
path('remove_from_wishlist/<int:id>/',views.remove_from_wishlist,name='remove_from_wishlist'),
#wishlist product count
path('wishlist_product_count/',views.wishlist_product_count,),

#cart
#cart page
path('cart/',views.user_cart,name='user_cart'),
#cart product count
path('variant_in_cart_status/',views.variant_in_cart_status),

#product adding in wish list
path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
#remove product from cart
path('remove_from_cart/<int:id>/',views.remove_from_cart,name='remove_from_cart'),
#cart product count
path('cart_product_count/',views.cart_product_count,),
#cart product qty update
path('cart_variant_qty_update/<int:id>/<int:quantity>/',views.cart_variant_qty_update),

#cart status
path('user_cart_status/',views.user_cart_status),


#add new address 
path('add_new_address_cart/',views.add_new_address_cart,name='add_new_address_cart'),
#update address
path('update_address_cart/<int:id>/',views.update_address_cart,name='update_address_cart'),
#delete address
path('delete_address_cart/<int:id>/',views.delete_address_cart,name='delete_address_cart'),
#set default address
path('default_address_cart/<int:id>/',views.default_address_cart,name='default_address_cart'),

#check variant qty for checkout page
path('get_variant_stock/<int:variant_id>/',views.get_variant_stock),


#orders
#order confirm
path('order_confirm/',order_confirm),
#order success 
path('order_success/<str:order_num>/',order_success),
#cancel order
path('cancel_order/<int:order_id>/<int:variant_id>/',cancel_order,name='cancel_order'),
#return order
path('return_order/<int:id>/',return_order,name='return_order'),
#order detail
path('order_detail/<int:order_id>/<int:variant_id>/',views.order_detail,name='order_detail'),

#generate pdf
 path('generate_pdf/<str:order_num>/', generate_pdf, name='generate_pdf'),

 #get rasor pay instance
 path('razor_pay_instance/',views.razor_pay_instance),

 #review 
 path('add_review/<int:variant_id>/',add_review,name="add_review"),

 path('delete_review/<int:id>/<int:variant_id>/',delete_review,name='delete_review'),

 path('update_review/<int:id>/<int:variant_id>/',update_review),







]