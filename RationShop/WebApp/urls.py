from tkinter.font import names

from django.urls import path
from WebApp import views

urlpatterns = [

    path('Home/', views.home, name='Home'),
    path('Products/', views.products, name='Products'),
    path('ContactUs/', views.contact_us, name='ContactUs'),
    path('SaveContact/', views.save_contact, name='SaveContact'),
    path('About/', views.about_page, name='About'),

    path('SignUpPage/', views.signup_page, name='SignUpPage'),
    path('SignUp/', views.save_signup, name='SignUp'),
    path('', views.login_page, name='LoginPage'),
    path('Login/', views.save_login, name='Login'),
    path('LogOut/', views.log_out, name='LogOut'),

    path('CartPage/', views.cart_page, name='CartPage'),
    path('SingleProduct/<int:si_id>/', views.single_product, name='SingleProduct'),
    path('Save_Cart/', views.save_cart, name='Save_Cart'),
    path('DeleteCart/<int:crt_id>/', views.delete_cart, name='DeleteCart'),

    path('Shop/', views.sin_up, name='Shop'),
    path('MyDetails/<int:my_id>/', views.my_details, name='MyDetails'),
    path('ShopHome/', views.shop_home, name='ShopHome'),
    path('SaveShop/', views.shop_signup, name='SaveShop'),

    path('OrderPage/', views.order_page, name='OrderPage'),

    path('CheckOut/', views.checkout_page, name='CheckOut'),
    path('Save_Checkout/', views.save_checkout, name='Save_Checkout'),

    path('ShopStock/', views.shop_stock, name='ShopStock'),
    path('ShopSingle/<int:s_id>/', views.shop_single_prod, name='ShopSingle'),

    path('Delivery_Partner/', views.delivery_partner, name='Delivery_Partner'),
    path('OrderStatus/<uuid:order_num>/', views.update_status, name='OrderStatus'),

    path('OrderDetails/<uuid:order_num>/', views.order_details, name='OrderDetails'),

    path('DeliverySignUp/', views.signup_delivery, name='Delivery_SignUp'),
    path('SaveDelivery_SignUp/', views.save_delivery_signup, name='SaveDelivery_SignUp'),

    path('PaymentPage/', views.payment_page, name='PaymentPage'),
    path('CancelPayment/', views.cancel_payment, name='CancelPayment'),

    path('Requests/', views.request_page, name='Requests'),
    path('Dashboard/', views.dashboard, name='Dashboard'),
    path('ApproveRequests/', views.approve_request, name='ApproveRequests'),
    path('PartnerDetails/', views.partner_details, name='PartnerDetails'),
    path('PendingRequests/', views.pending_requests, name='PendingRequests'),

]
