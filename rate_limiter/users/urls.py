from django.urls import path
from django.contrib.auth import views as auth_views

from .views import greet_user

urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('', greet_user, name="greet_user")
]
