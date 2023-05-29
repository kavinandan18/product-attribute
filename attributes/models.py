from django.db import models
from djongo import models as djongo_models
from bson.decimal128 import Decimal128

class Family(models.Model):
    name = models.CharField(max_length=50) # Laptop

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=50)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    id = djongo_models.ObjectIdField()
    name = models.CharField(max_length=50,null=True,blank=True)
    value = models.CharField(max_length=50,null=True,blank=True)
    product = djongo_models.ForeignKey('Product', on_delete=models.CASCADE, related_name='attributes')

class DecimalFields(models.DecimalField):
    def from_db_value(self,value,expression,connection):
        if isinstance(value,Decimal128):
            return float(value.to_decimal())
        return value

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price =DecimalFields(max_digits=8, decimal_places=2)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



