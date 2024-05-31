from django.urls import path
from . import views

app_name="manager_welcome"

urlpatterns=[
    path('', views.welcome_page, name='welcome-page'),
    path('send_email/', views.send_email, name='send-email'),
]