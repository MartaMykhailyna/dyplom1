from django.urls import path, include
from . import views

app_name = 'manager_add'

urlpatterns = [
    # path('', views.index, name='index'),
    path('items/add_item/', views.add_item, name='add-item'),
    path('orders/add_order/', views.add_order, name='add-order'),
    path('reservations/add_reservation/', views.add_reservation, name='add-reservation'),
    # path('users/add_user/', views.add_user, name='add-user'),
    # path('orders/add_order/', views.add_order, name='add-order'),
    # path('reservations/add_reservation/', views.add_reservation, name='add-reservation'),

    # path('orders/', views.orders, name='orders'),
    # path('reservations/', views.reservations, name='reservations'),
    # path('users/', views.users, name='users'),
    # path('analytics/', views.analytics, name='analytics'),
    # path('convert/<str:currency>/', views.convert_currency, name='convert_currency'),
]
