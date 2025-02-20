
from django.db import models

# Create your models here.




class StockCategory(models.Model):
    Category_Name = models.CharField(max_length=100)
    C_Description = models.CharField(max_length=150, null=True)
    Category_Image = models.ImageField(upload_to='Category Image',null=True)



class Stock(models.Model):
    Item = models.CharField(max_length=100)
    Description = models.CharField(max_length=150,null=True)
    Total_Quantity = models.IntegerField()
    Category = models.CharField(max_length=100)
    Availability = models.CharField(max_length=50)
    Item_Price = models.IntegerField(null=True)
    Item_Image = models.ImageField(upload_to='Item Image',null=True)

