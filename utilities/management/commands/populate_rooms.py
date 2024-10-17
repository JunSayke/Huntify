from django.core.management.base import BaseCommand
from faker import Faker
from booking_feature.models import BoardingHouse, Room, RoomImage
import random

class Command(BaseCommand):
    help = 'Populate the database with fake rooms and room images'

    def add_arguments(self, parser):
        parser.add_argument('num_entries', type=int, help='The number of rooms to create')

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_entries = kwargs['num_entries']

        # Ensure there is at least one boarding house in the database
        if not BoardingHouse.objects.exists():
            self.stdout.write(self.style.ERROR('No boarding houses found. Please populate boarding houses first.'))
            return

        for _ in range(num_entries):  # Use the specified number of entries
            # Get a random boarding house
            boarding_house = BoardingHouse.objects.order_by('?').first()
            room = Room.objects.create(
                boarding_house_id=boarding_house,
                name=fake.word(),
                price=fake.random_number(digits=5, fix_len=True) / 100,  # Random price between 0.00 and 999.99
                is_available=fake.boolean()
            )

            # Create RoomImage entries for the room
            for _ in range(random.randint(0,3)):  # Create 0-3 images per room
                RoomImage.objects.create(
                    room_id=room,
                    image=fake.image_url()  # Generate a fake image URL
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_entries} rooms with images.'))