from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register

app_name = 'user'

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(template_name='auth/login.html'),
         name='login'),
    path('register/', register, name='register'),
]