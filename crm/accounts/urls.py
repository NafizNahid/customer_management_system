from django.urls import path
from . import views

urlpatterns = [
    
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    
    
    path('', views.dashBoard, name="dashboard"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>/', views.customer, name="customer"),

    #------------ (CREATE URLS) ------------
    path('create_orde/', views.createOrder, name="create_order"),
    
   
    #------------ (UPDATE URLS) ------------
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),


    #------------ (UPDATE URLS) ------------
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    
    
    

]


