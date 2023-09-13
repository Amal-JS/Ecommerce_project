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


]