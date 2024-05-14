from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('admins_edit/', views.admins_edit, name='admins_edit'),
    # path('items/', views.items, name='items'),
    # path('orders/', views.orders, name='orders'),
    # path('reservations/', views.reservations, name='reservations'),
    # path('users/', views.users, name='users'),
    # path('analytics/', views.analytics, name='analytics'),
    # path('convert/<str:currency>/', views.convert_currency, name='convert_currency'),
]
