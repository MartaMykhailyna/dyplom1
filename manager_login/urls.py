from django.urls import path
from . import views

app_name='manager_login'

urlpatterns = [
    # path('login/', login, name='login'),
    path('login/', views.login, name='login'),
    path('register/', views.register_view, name='register'),
    
    # path('', users_login, name='users_login'),
]