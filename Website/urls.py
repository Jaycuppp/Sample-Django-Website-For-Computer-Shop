from . import views

from django.urls import path, include
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

urlpatterns = [
    path('', views.HomePage, name="HomePage"),
    path('AboutUs', views.AboutUsPage, name="AboutUsPage"),
    path('Products', views.ProductsPage, name="ProductsPage"),
    path('Services/Careers', views.Services_Careers, name="Careers"),
    path('Services/Careers/<Job_ID>', views.Services_Careers_Applying, name="JobApplication"),
    path('Services/Laboratory', views.Services_Laboratory, name="LaboratoryPage"),
    path('Services/TechSupport', views.Services_TechSupport, name="TechSupportPage"),
    path('Services/TechConsultation', views.Services_TechConsultation, name="TechConsultationPage"),
    path('Locations', views.LocationsPage, name="LocationPages"),
    path('ReviewForm', views.CustomerReviewFormPage, name="CustomerReviewsPage"),
    path('ShowLocation/<Location_ID>', views.ShowLocation, name="ShowLocationPage"),
    path('UpdateLocation/<Location_ID>', views.UpdateLocation, name="UpdateLocation"),
    path('DeleteLocation/<Location_ID>', views.DeleteLocation, name="DeleteLocation"),
    path('LocationPDFFile', views.LocationsPDF , name = 'LocationPDFFile'),
    path('ShowProduct/<Product_ID>', views.ShowProduct, name="ShowProductPage"),
    path('Reports', views.ReportsPage, name="Reports"),
    path('ProductTextFile', views.ProductText, name='ProductTextFile'),
    path('ProductCSVFile', views.ProductCSV, name='ProductCSVFile'),
    path('UpdateProduct/<Product_ID>', views.UpdateProduct, name="UpdateProduct"),
    path('DeleteProduct/<Product_ID>', views.DeleteProduct, name="DeleteProduct"),
    path('ProductSearch', views.ProductSearchPage, name="ProductSearchResultPage"),
    path('ProductAdd', views.ProductAddPage, name="AddProductPage"),
    path('PreOrder', views.AllPreOrder, name="AllPreOrder"),
    path('Promotions', views.AllPromotions, name="AllOnPromo"),
    path('ShoppingCart', views.ShopCart, name="ShoppingCart"),
    path('ShoppingCartAdd', views.ShoppingCartAdd, name="AddToShopCart"),
    path('ShoppingCartRemove', views.ShoppingCartRemove, name="RemoveFromShopCart"),
    path('ShoppingCartUpdate', views.ShoppingCartUpdate, name="UpdateShopCart"),
    path('ShoppingCartCheckOut', views.ShopCart_CheckOut, name="CheckingOut"),
    path('ShoppingCartBilling', views.ShopCartBilling, name="Billing"),
    path("Order_Processing", views.OnlineOrderProcessing, name="ProcessOrder"),
    path("Order_Single/<int:PrimeKey>", views.OnlineOrderSingle, name="OrderSingle"),
    path("Order_Shipped", views.OnlineOrderShipped, name="OrderShipped"),
    path("Order_Not_Shipped", views.OnlineOrderNotShipped, name="OrderNotShipped"),
    path('paypal', include("paypal.standard.ipn.urls")),
    path('Payment-Success/', views.PayPal_Successfull_Payment, name='PayPalPaymentSuccess'),
    path('Payment-Failure/', views.PayPal_Failure_Payment, name='PayPalPaymentFail'),
    path('AdminDash/ECommerce', views.AdminDashECommerce, name="AdminDashECommerce"),
    path('AdminDash/RetailStores', views.AdminDashRetailStores, name="AdminDashRetailStores"),
    path('AdminDash/CustomerSupportUpdate/<Ticket_ID>', views.AdminCustomerSupportUpdate, name="UpdateCSRTicket"),
    path('AdminDash/CustomerSupport', views.AdminDashCustomerSupport, name="AdminDashCustomerSupport"),
    path('AdminDash/HumanResources', views.AdminHumanResources, name="AdminHumanResources"),
    path('AdminDash/CustomerReviews', views.AdminCustomerReviews, name="AdminCustomerReviews"),
]
