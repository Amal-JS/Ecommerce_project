from django.urls import path
from . import views

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



#cart page
path('cart/',views.user_cart,name='user_cart'),



#checkout page
path('checkout/',views.user_checkout,name='user_checkout'),


#user profile views
path('dashboard/',views.user_profile_dashboard,name='user_profile_dashboard'),
path('orders/',views.user_profile_order,name='user_profile_orders'),
path('address/',views.user_profile_address,name='user_profile_address'),
path('account_details',views.user_profile_account_details,name='user_profile_account_details'),


#add new address 
path('add_new_address/',views.add_new_address,name='add_new_address'),
#update address
path('update_address/<int:id>/',views.update_address,name='update_address'),
#delete address
path('delete_address/<int:id>/',views.delete_address,name='delete_address'),
#set default address
path('default_address/<int:id>/',views.default_address,name='default_address'),
]