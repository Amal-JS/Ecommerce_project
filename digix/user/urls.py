from django.urls import path
from . import views


urlpatterns =[

path('',views.index,name='index'),
path('all_products',views.category_display_all_products,name='all_products')



]