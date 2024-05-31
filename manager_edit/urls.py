from django.urls import path, include
from . import views

app_name = 'manager_edit'

urlpatterns = [
    # path('', views.index, name='index'),
    path('update_item/<int:shoes_id>/', views.update_item, name='update-item'),
    path('users/update_user/<int:user_id>/', views.update_user, name='update-user'),
    path('orders/update_order/<int:order_id>/', views.update_order, name='update-order'),
    path('reservations/update_reservation/<int:reservation_id>/', views.update_reservation, name='update-reservation'),

    # path('orders/', views.orders, name='orders'),
    # path('reservations/', views.reservations, name='reservations'),
    # path('users/', views.users, name='users'),
    # path('analytics/', views.analytics, name='analytics'),
    # path('convert/<str:currency>/', views.convert_currency, name='convert_currency'),
]
