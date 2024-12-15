from django.db import models
from django.contrib.auth.models import *
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category/image",null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name = 'children', null=True)
    is_active = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name

class Product(models.Model):
    COLOR_FIELD = (
        ('RED', 'RED'),
        ('BLUE', 'BLUE'),
        ('YELLOW', 'YELLOW'),
        ('Orange', 'Orange'),
    )
    SIZE_FIELD = (
        ('RED', 'RED'),
        ('BLUE', 'BLUE'),
        ('YELLOW', 'YELLOW'),
        ('Orange', 'Orange'),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    brand = models.CharField(max_length=100, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    additional_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50, choices=COLOR_FIELD, null = True)
    size = models.CharField(max_length=50, choices=SIZE_FIELD, null = True)
    quantity = models.PositiveSmallIntegerField(null = True)
    stock = models.IntegerField()



    def save(self, *args, **kwargs):
        self.slug = self.name.replace(" ", "-").lower()
        super(Product, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"ID NO - {self.id}- {self.name}"
    


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)  
    updated = models.DateTimeField(auto_now = True)  
    session_key = models.CharField(max_length=250)

    def __str__(self):
        return f"Cart ID {self.id}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    

    def get_total(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        else:
            return self.product.price * self.quantity
    


