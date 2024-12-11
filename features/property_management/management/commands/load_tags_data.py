from django.core.management.base import BaseCommand
from features.property_management.models import Tag


class Command(BaseCommand):
    help = 'Populate the Tag model with initial data'

    def handle(self, *args, **kwargs):
        boarding_house_tags = [
            'WiFi',
            'Parking',
            'Laundry',
        ]

        boarding_room_tags = [
            'Air Conditioning',
            'WiFi',
            'Parking',
            'Laundry',
            'Fully Furnished',
            'Pet-Friendly',
            'En-suite Bathroom',
            'Kitchen Access',
            'Security Lock ',
            'Balcony',
            'Quiet Area',
            'City View',
            'Cable TV',
        ]

        self.helper_create_tags(boarding_house_tags, Tag.Type.BOARDING_HOUSE)
        self.helper_create_tags(boarding_room_tags, Tag.Type.BOARDING_ROOM)

    def helper_create_tags(self, tags, tag_type):
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name, type=tag_type)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created {tag_type} tag: {tag.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'{tag_type} tag already exists: {tag.name}'))
