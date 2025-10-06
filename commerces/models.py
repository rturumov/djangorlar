from django.db import models
from django.contrib.auth.models import User
from catalogs.models import Restaurant, MenuItem


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.city}, {self.street}, {self.building}"


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("confirmed", "Confirmed"),
        ("delivering", "Delivering"),
        ("done", "Done"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    promo_codes = models.ManyToManyField(PromoCode, through="OrderPromo")

    def __str__(self):
        return f"Order #{self.id} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item_name} x{self.quantity}"


class OrderItemOption(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="options")
    option_name = models.CharField(max_length=100)
    price_delta = models.DecimalField(max_digits=6, decimal_places=2, default=0)


class OrderPromo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    applied_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ("order", "promo_code")