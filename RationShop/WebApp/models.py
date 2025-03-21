from django.db import models
import uuid
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib.auth.models import User

class ShopOwner(models.Model):
    user = models.OneToOneField(
        User, null=True,
        on_delete=models.CASCADE,
        related_name='shopowner_profile'
    )
    S_Name = models.CharField(max_length=100)
    Reg_Num = models.CharField(max_length=100, unique=True)
    S_Mail = models.EmailField(max_length=100)
    S_Mobile = models.CharField(max_length=20)
    State = models.CharField(max_length=100, null=True)
    District = models.CharField(max_length=100, null=True)
    Taluk = models.CharField(max_length=100, null=True)
    Panchayat = models.CharField(max_length=100, null=True)
    Place = models.CharField(max_length=100, null=True)


    def __str__(self):
        return f'{self.Reg_Num}'


class BeneficiaryRegister(models.Model):
    user = models.OneToOneField(
        User, null=True,
        on_delete=models.CASCADE,
        related_name='beneficiary_profile'
    )
    U_Name = models.CharField(max_length=100)
    Ration_Card = models.CharField(max_length=100, unique=True)
    Card_Color = models.CharField(max_length=50, null=True)
    U_Mail = models.EmailField(max_length=100)
    U_Mobile = models.CharField(max_length=20)
    Family_Members = models.IntegerField(null=True)
    Shop_ID = models.CharField(max_length=100, null=True)
    is_approved = models.BooleanField(default=False)
    C_Pass = models.CharField(max_length=100, null=True)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return self.U_Name


class ContactDB(models.Model):
    F_Name = models.CharField(max_length=100)
    C_Mail = models.EmailField(max_length=100)
    Phn_Num = models.CharField(max_length=100)
    Mesg = models.CharField(max_length=150)


class CartDB(models.Model):
    order = models.ForeignKey(
        'WebApp.OrderDB',  # Keep the app name if OrderDB is in WebApp
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items'
    )
    User_Name = models.CharField(max_length=100)

    # Corrected ForeignKey to RationItems in AdminApp
    ration_item = models.ForeignKey(
        'AdminApp.RationItems',  # Specify 'AdminApp.RationItems' to reference model in AdminApp
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart_items'
    )

    # Corrected ForeignKey to Stock in AdminApp
    stock_item = models.ForeignKey(
        'AdminApp.Stock',  # Specify 'AdminApp.Stock' to reference model in AdminApp
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart_items'
    )

    Item_Name = models.CharField(max_length=100)  # You might not need this anymore if linked to RationItems/Stock
    Item_Quantity = models.IntegerField(null=True)
    I_Price = models.IntegerField(null=True,blank=True,default=0)
    I_Total = models.IntegerField()
    Item_Image = models.ImageField(
        upload_to="Cart Images")  # You might not need this if images are in RationItems/Stock

    class Meta:
        verbose_name = "Cart Item"


class OrderDB(models.Model):
    Order_Num = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    Shop = models.ForeignKey(
        ShopOwner,
        on_delete=models.CASCADE,
        related_name='orders',
        null=True
    )
    User_Name = models.CharField(max_length=100, null=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Address = models.CharField(max_length=150)
    Mobile = models.CharField(max_length=20)
    Card_Num = models.CharField(max_length=100, null=True)
    Reg_Num = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(
        max_length=50,
        choices=[('COD', 'Cash on Delivery'), ('Online', 'Online Payment')],
        default='COD'
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=100,
                                      choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed')],
                                      default='Pending', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"

    @property
    def total(self):
        return self.cart_items.aggregate(total=Sum('I_Total'))['total'] or 0



class OrderStatus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('out_for_delivery', 'Out For Delivery'),
        ('delivered', 'Delivered')
    ]

    order = models.OneToOneField(
        OrderDB,
        on_delete=models.CASCADE,
        related_name='status'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Order Statuses"


class Delivery(models.Model):
    D_Partner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='delivery_profile'
    )
    D_Shop = models.ForeignKey(
        ShopOwner,
        on_delete=models.CASCADE,
        related_name='delivery_partners'
    )
    D_Phone = models.CharField(max_length=20)
    D_Pic = models.ImageField(upload_to="Delivery Partner", null=True, blank=True)


class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField()

    def is_valid(self):
        return now() < self.otp_expiry
