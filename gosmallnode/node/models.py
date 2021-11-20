from django.db import models

class Category(models.Model):
    categoryName = models.CharField(max_length=100)

class Company(models.Model):
    companyName = models.CharField(max_length=100)
    companyCategory = models.ForeignKey(Category, on_delete=models.PROTECT)
    ip = models.CharField(max_length=100)
    identity = models.CharField(max_length=32) # hexdigest of md5 name + ip

class Product(models.Model):
    productImage = models.CharField(max_length=1000)
    productName = models.CharField(max_length=100)
    productTags = models.CharField(max_length=300)
    manufacturer = models.ForeignKey(Company, on_delete=models.CASCADE)

class CreationCodes(models.Model):
    code = models.CharField(max_length=36)

class Self(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)