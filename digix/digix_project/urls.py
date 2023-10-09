from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.views.defaults import page_not_found

urlpatterns = [
    path('built_in_admin/', admin.site.urls),
    path('admin/',include('digix_admin.urls')),
    path('',include('user.urls')),
    path('product/',include('products.urls'))
]

# Define a custom handler404 view and specify the custom template for 404 errors
handler404 = 'user.views.custom_404_view'  # Replace 'yourapp.views.custom_404_view' with the actual view function you want to use for custom handling of 404 errors


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)