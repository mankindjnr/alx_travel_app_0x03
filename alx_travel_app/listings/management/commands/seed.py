import random
import uuid
from datetime import timedelta, date
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from listings.models import Listing, Booking
from users.models import User  # Adjust the path if User is in another app


class Command(BaseCommand):
    help = "Seed the database with sample data for Listings and Bookings."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding the database...")
        self.seed_users()
        self.seed_listings()
        self.seed_bookings()
        self.stdout.write("Database seeded successfully!")

    def seed_users(self):
        if User.objects.exists():
            self.stdout.write("Users already exist. Skipping user seeding.")
            return

        self.stdout.write("Creating sample users...")
        users = [
            User(
                user_id=uuid.uuid4(),
                first_name=f"User{i}",
                last_name=f"Last{i}",
                email=f"user{i}@example.com",
                phone_number=f"+25470000{i}",
                role="host" if i % 2 == 0 else "guest",
            )
            for i in range(1, 6)
        ]
        User.objects.bulk_create(users)
        self.stdout.write("Sample users created.")

    def seed_listings(self):
        if Listing.objects.exists():
            self.stdout.write("Listings already exist. Skipping listing seeding.")
            return

        self.stdout.write("Creating sample listings...")
        hosts = User.objects.filter(role="host")
        listings = [
            Listing(
                property_id=uuid.uuid4(),
                host=random.choice(hosts),
                title=f"Sample Listing {i}",
                description="A beautiful place to stay.",
                price_per_night=random.randint(50, 300),
            )
            for i in range(1, 11)
        ]
        Listing.objects.bulk_create(listings)
        self.stdout.write("Sample listings created.")

    def seed_bookings(self):
        if Booking.objects.exists():
            self.stdout.write("Bookings already exist. Skipping booking seeding.")
            return

        self.stdout.write("Creating sample bookings...")
        guests = User.objects.filter(role="guest")
        listings = Listing.objects.all()
        bookings = []

        for _ in range(10):
            start_date = date.today() + timedelta(days=random.randint(1, 30))
            end_date = start_date + timedelta(days=random.randint(1, 7))
            total_price = random.randint(100, 1000)

            bookings.append(
                Booking(
                    booking_id=uuid.uuid4(),
                    property=random.choice(listings),
                    user=random.choice(guests),
                    start_date=start_date,
                    end_date=end_date,
                    total_price=total_price,
                    status=random.choice(["pending", "confirmed", "canceled"]),
                )
            )

        Booking.objects.bulk_create(bookings)
        self.stdout.write("Sample bookings created.")
