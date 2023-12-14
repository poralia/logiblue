from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('apps.authbase.urls')),
]
