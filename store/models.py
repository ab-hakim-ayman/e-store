from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to="customer/", blank=True, null=True)
    mobile = models.CharField(max_length=16)
    address = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def createCustomer(sender, instance, created, *args, **kwargs):
    if created:
        Customer.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=Customer)
def createUsername(sender, instance, created, *args, **kwargs):
    if created:
        instance.username = instance.email
        instance.save()


class Category(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='brand/', blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='product/')
    old_price = models.FloatField(blank=True, null=True)
    price = models.FloatField()
    discount = models.PositiveIntegerField(default=0)
    category = models.ManyToManyField(Category)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, blank=True, null=True)
    details = models.TextField()
    tags = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class View(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    view = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.title


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    text = models.TextField()


class Slider(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='slider/')
    url = models.URLField(default='#')
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Trending(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.FloatField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.user.email


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ManyToManyField(Product)
    quantity = models.IntegerField()
    total = models.FloatField()


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=16)
    address = models.TextField()
    email = models.CharField(max_length=160)
    order_status = models.CharField(
        max_length=100, choices=ORDER_STATUS, default="Order Received")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.created_at