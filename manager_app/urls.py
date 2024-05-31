from django.urls import path
from . import views

app_name='manager_app'

urlpatterns = [
    path('analytics_admin/', views.analytics_for_admin, name='analytics-for-admin'),
    path('analytics_user/', views.analytics_for_user, name='analytics-for-user'),
    # path('', views.analytics, name='analytics'),
    # path('api/order_sums_by_month/', order_sums_by_month, name='order_sums_by_month'),
    path('items/', views.items, name='items'),
    # path('update_item/<int:shoes_id>/', views.update_item, name='update-item'),
    path('det/<int:id>/', views.items_detailed_view, name='items-photos'),
    path('items/delete/<int:shoes_id>/', views.items_delete, name='items-delete'),
    # path('edit/<int:id>/', views.items_form_edit, name='items-form-edit'),
    path('users/', views.users, name='users'),
    path('users_toggle_status/<int:user_id>/', views.users_toggle_status, name='users_toggle_status'),
    path('users/delete/<int:user_id>/', views.users_delete, name='users-delete'),
    # path('users/update_user/<int:user_id>/', views.update_user, name='update-user'),
    path('orders/', views.orders, name='orders'),
    path('orders-detail/<int:id>/', views.orders_detailed_view, name='orders-detail'),
    path('orders/delete/<int:order_id>/', views.orders_delete, name='orders-delete'),
    # path('orders/update_order/<int:order_id>/', views.update_order, name='update-order'),
    # path("order-sum/", views.order_sum_view, name="order-sum"),
    path('reservations/', views.reservations, name='reservations'),
    path('reservations/delete/<int:reservation_id>/', views.reservations_delete, name='reservations-delete'),
    # path('reservations/update_reservation/<int:reservation_id>/', views.update_reservation, name='update-reservation'),
    # path('convert/<str:currency>/', views.convert_currency, name='convert_currency'),
]
 