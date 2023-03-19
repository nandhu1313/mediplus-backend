from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    title = models.CharField(max_length=255)
    orp = models.CharField(max_length=255)
    mrp = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="product-image")
    def __str__(self) -> str:
        return self.title
