from datetime import date
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random


from accounts.models import CustomUser

fake = Faker()


class Command(BaseCommand):
    help = "Generate 10,000 users"

    def handle(self, *args, **kwargs):
        batch_size = 1000
        total_users = 10000

        departments = ["IT", "HR", "Sales", "Finance"]
        roles = ["admin", "manager", "employee"]

        password = "12345"

        self.stdout.write("Preparing password hash...")
        temp_user = CustomUser()
        temp_user.set_password(password)
        hashed_password = temp_user.password

        users = []

        for i in range(total_users):
            user = CustomUser(
                email=fake.unique.email(),
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                city=fake.city(),
                country=fake.country(),
                department=random.choice(departments),
                role=random.choice(roles),
                birth_date=fake.date_between(
                    start_date=date(1975, 1, 1),
                    end_date=date(2005, 12, 31)
                ),
                salary=random.randint(200000, 900000),
                password=hashed_password,   
            )
            users.append(user)

            if len(users) == batch_size:
                CustomUser.objects.bulk_create(users)
                users.clear()
                self.stdout.write(f"Inserted {i + 1} users...")

        if users:
            CustomUser.objects.bulk_create(users)

        self.stdout.write(self.style.SUCCESS("Generated 10,000 users!"))