from django.urls import path
from manager_login.views import *

urlpatterns = [
    path('', login, name='login'),
    # path('', users_login, name='users_login'),
]