from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('built_in_admin/', admin.site.urls),
    path('admin/',include('digix_admin.urls')),
    path('',include('user.urls')),
    path('product/',include('products.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)