from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from booking_feature.models import BoardingHouse, Room, BoardingHouseImage, RoomImage

class Command(BaseCommand):
    help = 'Create landlord group and assign permissions'

    def handle(self, *args, **kwargs):
        # Create a new group
        group, created = Group.objects.get_or_create(name='landlord')

        if created:
            self.stdout.write(self.style.SUCCESS('Group "landlord" created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Group "landlord" already exists'))

        # List of models and their permissions to assign
        models_permissions = {
            BoardingHouse: [
                'add_boardinghouse',
                'change_boardinghouse',
                'delete_boardinghouse',
                'view_boardinghouse',
            ],
            Room: [
                'add_room',
                'change_room',
                'delete_room',
                'view_room',
            ],
            BoardingHouseImage: [
                'add_boardinghouseimage',
                'change_boardinghouseimage',
                'delete_boardinghouseimage',
                'view_boardinghouseimage',
            ],
            RoomImage: [
                'add_roomimage',
                'change_roomimage',
                'delete_roomimage',
                'view_roomimage',
            ],
        }

        # Assign permissions to the group for each model
        for model, permissions in models_permissions.items():
            content_type = ContentType.objects.get_for_model(model)
            for perm in permissions:
                permission = Permission.objects.get(codename=perm, content_type=content_type)
                group.permissions.add(permission)

        # Save the group
        group.save()
        self.stdout.write(self.style.SUCCESS('Permissions assigned to group "landlord"'))