from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)

    categories = models.ManyToManyField(Category, through="ItemCategory")
    options = models.ManyToManyField(Option, through="ItemOption")

    def __str__(self):
        return self.name


class ItemCategory(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("item", "category")


class ItemOption(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    price_delta = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ("item", "option")