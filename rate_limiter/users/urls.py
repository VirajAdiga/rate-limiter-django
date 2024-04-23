from django.urls import path
from django.contrib.auth import views as auth_views

from .views import greet_user, greet_public_user

urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('public', greet_public_user, name='greet-public-user'),
    path('', greet_user, name="greet-user")
]
