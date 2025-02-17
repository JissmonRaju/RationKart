from django.urls import path
from WebApp import views

urlpatterns = [

    path('Home/', views.home, name='Home'),
    path('Products/', views.products, name='Products'),
    path('ContactUs/', views.contact_us, name='ContactUs'),
    path('SaveContact/',views.save_contact,name='SaveContact'),
    path('About/',views.about_page,name='About'),

    path('SignUpPage/', views.signup_page, name='SignUpPage'),
    path('SignUp/',views.save_signup,name='SignUp'),
    path('LoginPage/', views.login_page, name='LoginPage'),
    path('Login/',views.save_login,name='Login'),
    path('LogOut/',views.log_out,name='LogOut'),

    path('CartPage/',views.cart_page,name='CartPage')



]
