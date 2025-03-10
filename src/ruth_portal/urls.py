from django.contrib import admin
from django.urls import path, include
from .views import root_redirect_view, welcome_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', root_redirect_view, name="root_redirect"),
   
    path("welcome/", welcome_view, name="welcome"), 

    
]