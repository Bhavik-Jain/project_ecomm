from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('profile/', views.profilePage, name="profile"),
    path('order_history/', views.order_history, name='order_history'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('home/', views.store, name='store'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
]