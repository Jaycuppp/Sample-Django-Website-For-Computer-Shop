from django.urls import path
from . import views

urlpatterns = [
    path('CreateUser', views.User_Register , name='CreateAccount'),
    path('UserLogin', views.Login_Auth, name='LoginPage'),
    path('UserLogout', views.User_Logout, name='LogoutPage'),
    path('Account/MyAccount', views.AccountPage, name="MyAccountPage"),
    path('Account/MyAccountPasswordReset', views.AccountPasswordReset, name="MyAccountPasswordReset"),
    path('Account/MyAccountProfileUpdate', views.AccountProfileUpdate, name="MyAccountProfileUpdate"),
    path('Account/MySupport', views.MySupport, name="MySupportPage"),
]