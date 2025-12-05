from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.


class Customer(models.Model):
    mobile_number = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField()
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='customer')

    def __str__(self):
         return f"{self.age} {self.gender}"


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    available = models.BooleanField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return f"{self.product_name}"

# booking table structure

class Booking(models.Model):
    # Foreign keys
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,related_name='customer_bookings')
    product = models.ForeignKey('Product', on_delete=models.CASCADE,related_name='product_bookings')

    # Booking details
    email = models.EmailField()
    alt_mobile = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    # Order details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Status fields
    payment_status = models.CharField(
        max_length=20,
        default='pending'
    )

    order_status = models.CharField(
        max_length=20,
        default='pending'
    )

    payment_method = models.CharField(
        max_length=20,
        default='upi'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.customer}"


# class Bookingdetail(models.Model):
