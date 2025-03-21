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
    path('SaveSignUp/', views.save_signup, name='SaveSignUp'),
    path('PendingApproval/', views.pending_approval, name='PendingApproval'),
    path('check-approval-status/', views.check_approval_status, name='check_approval_status'),
    path('final_status/<int:beneficiary_id>/', views.final_status, name='Status'),

    # Login
    path('', views.login_page, name='LoginPage'),
    path('Login/', views.save_login, name='Login'),
    path('LogOut/', views.log_out, name='LogOut'),

    # Shop Owner side
    path('ApproveRequests/', views.pending_requests, name='ApproveRequests'),
    path('approve/<int:beneficiary_id>/', views.approve_beneficiary, name='approve_beneficiary'),
    path('reject/<int:beneficiary_id>/', views.reject_beneficiary, name='reject_beneficiary'),



    path('CartPage/', views.cart_page, name='CartPage'),
    path('SingleProduct/<int:si_id>/', views.single_product, name='SingleProduct'),
    path('Save_Cart/', views.save_cart, name='Save_Cart'),
    path('DeleteCart/<int:crt_id>/', views.delete_cart, name='DeleteCart'),

    path('Shop/', views.sin_up, name='Shop'),
    path('MyDetails/<int:my_id>/', views.my_details, name='MyDetails'),
    path('SaveShop/', views.shop_signup, name='SaveShop'),
    path('ShopHome/', views.shop_home, name='ShopHome'),

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
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('CancelPayment/', views.cancel_payment, name='CancelPayment'),

    path('Requests/', views.request_page, name='Requests'),

    path('PartnerDetails/', views.delivery_partner_list, name='PartnerDetails'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),

    path('verify_shop_otp/',views.verify_shop_otp,name='verify_shop_otp')





]
