from django.core.management.base import BaseCommand
from catalogs.models import Restaurant, Category, Option, MenuItem, ItemCategory, ItemOption
from faker import Faker
import random
from decimal import Decimal

fake = Faker()

class Command(BaseCommand):
    help = "Generate 20 test records for all catalogs models"

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating test data for catalogs...")

        # Очистим старые тестовые данные
        ItemOption.objects.all().delete()
        ItemCategory.objects.all().delete()
        MenuItem.objects.all().delete()
        Option.objects.all().delete()
        Category.objects.all().delete()
        Restaurant.objects.all().delete()

        # Restaurants
        restaurants = [
            Restaurant.objects.create(
                name=fake.company(),
                description=fake.text()
            )
            for _ in range(20)
        ]

        # Categories
        categories = [
            Category.objects.create(name=fake.word().capitalize())
            for _ in range(20)
        ]

        # Options
        options = [
            Option.objects.create(name=fake.word().capitalize())
            for _ in range(20)
        ]

        # Menu Items
        items = []
        for _ in range(20):
            item = MenuItem.objects.create(
                restaurant=random.choice(restaurants),
                name=fake.word().capitalize(),
                description=fake.text(),
                base_price=Decimal(random.uniform(5, 50)).quantize(Decimal("0.01")),
                available=random.choice([True, False]),
            )
            items.append(item)

        # ItemCategory
        for item in items:
            for category in random.sample(categories, k=random.randint(1, 3)):
                ItemCategory.objects.create(
                    item=item,
                    category=category,
                    position=random.randint(1, 10)
                )

        # ItemOption
        for item in items:
            for option in random.sample(options, k=random.randint(1, 3)):
                ItemOption.objects.create(
                    item=item,
                    option=option,
                    price_delta=Decimal(random.uniform(0, 5)).quantize(Decimal("0.01")),
                    is_default=random.choice([True, False]),
                )

        self.stdout.write(self.style.SUCCESS("✅ Successfully generated 20 test records for all catalogs models."))