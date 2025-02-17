from django.db import models

# Create your models here.

class UserRegister(models.Model):
    U_Name = models.CharField(max_length=100)
    Ration_Card = models.CharField(max_length=100)
    U_Mail = models.EmailField(max_length=100)
    U_Mobile = models.CharField(max_length=20)
    U_Pass = models.CharField(max_length=100)
    C_Pass = models.CharField(max_length=100)


class ContactDB(models.Model):
    F_Name = models.CharField(max_length=100)
    C_Mail = models.EmailField(max_length=100)
    Phn_Num = models.CharField(max_length=100)
    Mesg = models.CharField(max_length=150)