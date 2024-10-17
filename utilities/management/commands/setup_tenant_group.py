from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from booking_feature.models import BoardingHouse, Room, BoardingHouseImage, RoomImage

class Command(BaseCommand):
    help = 'Create landlord group and assign permissions'

    def handle(self, *args, **kwargs):
        # Create a new group
        group, created = Group.objects.get_or_create(name='tenant')

        if created:
            self.stdout.write(self.style.SUCCESS('Group "tenant" created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Group "tenant" already exists'))

        # List of models and their permissions to assign
        models_permissions = {
            BoardingHouse: [
                'view_boardinghouse',
            ],
            Room: [
                'view_room',
            ],
            BoardingHouseImage: [
                'view_boardinghouseimage',
            ],
            RoomImage: [
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
        self.stdout.write(self.style.SUCCESS('Permissions assigned to group "tenant"'))