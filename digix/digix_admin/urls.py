from django.urls import path
from . import views
urlpatterns = [
    path('',views.admin_home,name='admin_home'),
    path('admin_login/',views.admin_login,name='admin_login')
]