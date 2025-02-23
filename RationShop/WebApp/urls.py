from tkinter.font import names

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
    path('', views.login_page, name='LoginPage'),
    path('Login/',views.save_login,name='Login'),
    path('LogOut/',views.log_out,name='LogOut'),

    path('CartPage/',views.cart_page,name='CartPage'),
    path('SingleProduct/<int:si_id>/',views.single_product,name='SingleProduct'),
    path('Save_Cart/',views.save_cart,name='Save_Cart'),
    path('DeleteCart/<int:crt_id>/',views.delete_cart,name='DeleteCart'),
    
    path('Shop/',views.sin_up,name='Shop'),
    path('MyDetails/<int:my_id>/',views.my_details,name='MyDetails'),
    path('ShopHome/',views.shop_home,name='ShopHome'),
    path('SaveShop/',views.shop_signup,name='SaveShop'),

    path('OrderPage/',views.order_page,name='OrderPage'),

    path('CheckOut/',views.checkout_page,name='CheckOut')





]
