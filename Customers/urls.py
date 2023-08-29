from django.urls import path
from . import views

urlpatterns = [
    path('UserLogin', views.Login_Auth, name='LoginPage'),
    path('UserLogout', views.User_Logout, name='LogoutPage'),
    path('CreateUser', views.User_Register , name='CreateAccount'),
]