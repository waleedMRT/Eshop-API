from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100 , blank=False , default="")
    description = models.TextField(max_length=1000 , blank=False , default="")
    price = models.DecimalField(max_digits=7 , decimal_places=2 )
    created_at = models.DateTimeField(auto_now_add=True)
    brand = models.CharField(max_length=20 , blank=True , null=True)
    rating = models.DecimalField(max_digits=3 , decimal_places=2 , default=0)
    rating_num = models.IntegerField(default=0)
    category = models.ForeignKey(Category , on_delete=models.SET_NULL , null=True )
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    image = CloudinaryField('image' , null=True , blank=True)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='reviews')
    rating = models.DecimalField(max_digits=3 , decimal_places=2)
    comment = models.TextField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user} , {self.rating}'
    


class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    totla_price = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} | {self.id}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name='items')
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10 , decimal_places=2)


    def __str__(self):
        return f'{self.price} x {self.quantity}'


# Create your models here.
