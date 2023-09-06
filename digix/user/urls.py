from django.urls import path
from . import views

app_name='user'

urlpatterns =[

#home page
path('',views.index,name='index'),

#get all products
path('all_products/',views.category_display_all_products,name='all_products'),

#get specafic product
path('product/',views.product,name="product"),

#user login , sign up , logout
path('user_sign_in/',views.user_sign_in,name='user_sign_in'),
path('user_sign_up/',views.user_sign_up,name='user_sign_up'),
path('user_logout/',views.user_logout,name='user_logout')

]