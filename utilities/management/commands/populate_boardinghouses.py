from django.core.management.base import BaseCommand
from faker import Faker
from authentication_feature.models import CustomUser
from booking_feature.models import BoardingHouse, BoardingHouseImage
import random

class Command(BaseCommand):
    help = 'Populate the database with fake boarding houses and boarding house images'

    def add_arguments(self, parser):
        parser.add_argument('num_entries', type=int, help='The number of boarding houses to create')

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_entries = kwargs['num_entries']

        # Ensure there is at least one user in the database
        if not CustomUser.objects.exists():
            CustomUser.objects.create_user(username='testuser', password='testuser')

        for _ in range(num_entries):  # Use the specified number of entries
            # Get a random user
            user = CustomUser.objects.order_by('?').first()
            boarding_house = BoardingHouse.objects.create(
                account_id=user,
                name=fake.company(),
                address=fake.address(),
                description=fake.text(),
            )

            # Create BoardingHouseImage entries for the boarding house
            for _ in range(random.randint(0,3)):  # Create 0-3 images per boarding house
                BoardingHouseImage.objects.create(
                    boarding_house_id=boarding_house,
                    image=fake.image_url()  # Generate a fake image URL
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {num_entries} fake boarding houses and images'))