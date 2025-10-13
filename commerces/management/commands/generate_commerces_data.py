from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalogs.models import Restaurant
from commerces.models import Address, PromoCode, Order, OrderItem, OrderItemOption, OrderPromo
from faker import Faker
from decimal import Decimal
import random

fake = Faker()

class Command(BaseCommand):
    help = "Generate 20 test records for all commerces models"

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating test data for commerces...")

        # Очистим старые тестовые данные
        OrderItemOption.objects.all().delete()
        OrderItem.objects.all().delete()
        OrderPromo.objects.all().delete()
        Order.objects.all().delete()
        PromoCode.objects.all().delete()
        Address.objects.all().delete()

        # Убедимся, что есть хотя бы один пользователь
        if not User.objects.exists():
            for i in range(5):
                User.objects.create_user(
                    username=f"user{i}",
                    email=f"user{i}@test.com",
                    password="password123"
                )

        users = list(User.objects.all())
        restaurants = list(Restaurant.objects.all())

        # Addresses
        addresses = [
            Address.objects.create(
                user=random.choice(users),
                city=fake.city(),
                street=fake.street_name(),
                building=str(random.randint(1, 100))
            )
            for _ in range(20)
        ]

        # PromoCodes
        promo_codes = [
            PromoCode.objects.create(
                code=f"PROMO{random.randint(1000,9999)}",
                discount_percent=random.randint(5, 30)
            )
            for _ in range(20)
        ]

        # Orders
        orders = []
        for _ in range(20):
            order = Order.objects.create(
                user=random.choice(users),
                restaurant=random.choice(restaurants) if restaurants else None,
                address=random.choice(addresses),
                status=random.choice(["new", "confirmed", "delivering", "done"]),
                subtotal=Decimal(random.uniform(10, 100)).quantize(Decimal("0.01")),
                discount_total=Decimal(random.uniform(1, 10)).quantize(Decimal("0.01")),
                total=Decimal(random.uniform(10, 150)).quantize(Decimal("0.01")),
            )
            orders.append(order)

        # Order Items
        order_items = []
        for order in orders:
            for _ in range(random.randint(1, 3)):
                item = OrderItem.objects.create(
                    order=order,
                    item_name=fake.word().capitalize(),
                    item_price=Decimal(random.uniform(5, 30)).quantize(Decimal("0.01")),
                    quantity=random.randint(1, 5),
                    line_total=Decimal(random.uniform(5, 150)).quantize(Decimal("0.01")),
                )
                order_items.append(item)

        # Order Item Options
        for item in order_items:
            for _ in range(random.randint(0, 2)):
                OrderItemOption.objects.create(
                    order_item=item,
                    option_name=fake.word().capitalize(),
                    price_delta=Decimal(random.uniform(0, 5)).quantize(Decimal("0.01")),
                )

        # Order Promos
        for order in random.sample(orders, k=10):
            OrderPromo.objects.create(
                order=order,
                promo_code=random.choice(promo_codes),
                applied_amount=Decimal(random.uniform(1, 10)).quantize(Decimal("0.01")),
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully generated 20 test records for all commerces models."))