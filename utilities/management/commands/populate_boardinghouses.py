from django.core.management.base import BaseCommand
from faker import Faker
from booking_feature.models import BoardingHouse
from authentication_feature.models import CustomUser

class Command(BaseCommand):
    help = 'Populate the boardinghouses database with fake data'

    def add_arguments(self, parser):
        parser.add_argument(
            'num_entries',
            type=int,
            help='The number of boardinghouses to create'
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_entries = kwargs['num_entries']

        # Ensure there is at least one user in the database
        if not CustomUser.objects.exists():
            CustomUser.objects.create_user(username='testuser', password='testuser')

        for _ in range(num_entries):  # Use the specified number of entries
            # Get a random user
            user = CustomUser.objects.order_by('?').first()
            BoardingHouse.objects.create(
                account_id=user,
                name=fake.company(),
                address=fake.address(),
                description=fake.text(),
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {num_entries} fake boardinghouses'))