from django.db import models
import uuid
from django.db.models import Sum


# Create your models here.
class ShopOwner(models.Model):
    S_Name = models.CharField(max_length=100)
    Reg_Num = models.CharField(max_length=100, unique=True)
    S_Mail = models.EmailField(max_length=100)
    S_Mobile = models.CharField(max_length=20)
    S_Pass = models.CharField(max_length=100)


class BeneficiaryRegister(models.Model):
    U_Name = models.CharField(max_length=100)
    Ration_Card = models.CharField(max_length=100, unique=True)
    Card_Color = models.CharField(max_length=50, null=True)
    U_Mail = models.EmailField(max_length=100)
    U_Mobile = models.CharField(max_length=20)
    U_Pass = models.CharField(max_length=100)
    Family_Members = models.IntegerField(null=True)


class ContactDB(models.Model):
    F_Name = models.CharField(max_length=100)
    C_Mail = models.EmailField(max_length=100)
    Phn_Num = models.CharField(max_length=100)
    Mesg = models.CharField(max_length=150)


class CartDB(models.Model):
    order = models.ForeignKey(
        'OrderDB',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart_items'
    )
    User_Name = models.CharField(max_length=100)
    Item_Name = models.CharField(max_length=100)
    Item_Quantity = models.IntegerField(null=True)
    I_Price = models.IntegerField()
    I_Total = models.IntegerField()
    Item_Image = models.ImageField(upload_to="Cart Images")

    class Meta:
        verbose_name = "Cart Item"


class OrderDB(models.Model):
    Order_Num = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    User_Name = models.CharField(max_length=100,null=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Address = models.CharField(max_length=150)
    Mobile = models.CharField(max_length=20)
    Card_Num = models.CharField(max_length=100,null=True)
    Reg_Num = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

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
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Order Statuses"
