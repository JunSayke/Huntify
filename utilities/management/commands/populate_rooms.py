from django.core.management.base import BaseCommand
from faker import Faker
from booking_feature.models import Room, BoardingHouse

class Command(BaseCommand):
    help = 'Populate the rooms database with fake data'

    def add_arguments(self, parser):
        parser.add_argument(
            'num_entries',
            type=int,
            help='The number of rooms to create'
        )

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
            Room.objects.create(
                boarding_house_id=boarding_house,
                name=fake.word(),
                price=fake.random_number(digits=5, fix_len=True) / 100,  # Random price between 0.00 and 999.99
                is_available=fake.boolean()
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_entries} rooms.'))