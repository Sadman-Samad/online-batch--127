from django.db import models
from django.contrib.auth.models import *
import cloudinary
import cloudinary.models
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    # image = models.ImageField(upload_to="category/image",null=True)
    image = cloudinary.models.CloudinaryField("category/image", blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name = 'children', null=True, blank=True)
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
    # image = models.ImageField(upload_to='products/', blank=True, null=True)
    image = cloudinary.models.CloudinaryField('products/', blank=True, null=True)
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
    


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    limit = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField()

    
    def __str__(self):
        return self.code
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=("pro"), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.product.name
     

class Order(models.Model):
    STATUS_CHOICE = [
        ('PENDING','PENDING'),
        ('PROCESSING','PROCESSING'),
        ('Complete','Complete'),
        ('Cancelled','Cancelled'),
    ]     

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICE, max_length=250, default='PENDING')
    cart = models.ManyToManyField(CartItem, blank =True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null = True, blank =True)
    full_name = models.CharField(max_length=250)
  
    address = models.TextField()
    phone = models.CharField(max_length=250, null=True)
    order_note = models.TextField(null=True)
    total_due = models.FloatField(null=True)
    total_paid = models.FloatField(null=True)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)