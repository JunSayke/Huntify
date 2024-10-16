from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from authentication_feature.models import CustomUser
from booking_feature.models import BoardingHouse

class Command(BaseCommand):
    help = 'Create a group and assign permissions'

    def handle(self, *args, **kwargs):
        # Create a new group
        group, created = Group.objects.get_or_create(name='landlord')

        if created:
            self.stdout.write(self.style.SUCCESS('Group "landlord" created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Group "landlord" already exists'))

        # Get the content type for the model you want to assign permissions to
        content_type = ContentType.objects.get_for_model(BoardingHouse)

        # List of permissions to assign
        permissions = [
            'add_BoardingHouse',
            'change_BoardingHouse',
            'delete_BoardingHouse',
            'view_mymodel',
        ]

        # Assign permissions to the group
        for perm in permissions:
            permission = Permission.objects.get(codename=perm, content_type=content_type)
            group.permissions.add(permission)

        # Save the group
        group.save()
        self.stdout.write(self.style.SUCCESS('Permissions assigned to group "my_group"'))