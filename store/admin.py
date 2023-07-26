from django.contrib import admin
from .models import (
    Customer,
    Category,
    Brand,
    Product,
    View,
    Review,
    Slider,
    Trending,
    Cart,
    CartItem,
    Order,
)

admin.site.register([
    Customer,
    Category,
    Brand,
    Product,
    View,
    Review,
    Slider,
    Trending,
    Cart,
    CartItem,
    Order,
])