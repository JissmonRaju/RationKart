
from django.db import models
import uuid
from django.contrib.gis.db import models as geomodels

# Create your models here.
class ShopOwner(models.Model):
    S_Name = models.CharField(max_length=100)
    Reg_Num = models.CharField(max_length=100,unique=True)
    S_Mail = models.EmailField(max_length=100)
    S_Mobile = models.CharField(max_length=20)
    S_Pass = models.CharField(max_length=100)
    Location = geomodels.PointField(null=True, blank=True)



class BeneficiaryRegister(models.Model):
    U_Name = models.CharField(max_length=100)
    Ration_Card = models.CharField(max_length=100,unique=True)
    Card_Color = models.CharField(max_length=50,null=True)
    U_Mail = models.EmailField(max_length=100)
    U_Mobile = models.CharField(max_length=20)
    U_Pass = models.CharField(max_length=100)
    Family_Members = models.IntegerField(null=True)
    Location = geomodels.PointField(null=True, blank=True)
    Assigned_Shop = models.ForeignKey(ShopOwner, on_delete=models.SET_NULL, null=True, blank=True)


class ContactDB(models.Model):
    F_Name = models.CharField(max_length=100)
    C_Mail = models.EmailField(max_length=100)
    Phn_Num = models.CharField(max_length=100)
    Mesg = models.CharField(max_length=150)


class CartDB(models.Model):
    User_Name = models.CharField(max_length=100)
    Item_Name = models.CharField(max_length=100)
    Item_Quantity = models.IntegerField(null=True)
    I_Price = models.IntegerField()
    I_Total = models.IntegerField()
    Item_Image = models.ImageField(upload_to="Cart Images")

class OrderDB(models.Model):
    Order_Num = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    Name = models.CharField(max_length=100)
    Card_Num = models.CharField(max_length=100,blank=True)
    Reg_Num = models.CharField(max_length=100,blank=True)
    Email = models.EmailField(max_length=100)
    Address = models.CharField(max_length=150)
    Mobile = models.CharField(max_length=20)






