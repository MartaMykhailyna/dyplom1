from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('manager_welcome.urls')),
    path('app/', include('manager_app.urls')),
    path('add/', include('manager_add.urls')),
    path('edit/', include('manager_edit.urls')),
    path('authorization/', include('manager_login.urls')),
    path('currency/', include('currency_exchange.urls')),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)