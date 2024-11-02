from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import Tenant, Landlord, Admin


def assign_group(instance, created, permissions):
    if created:
        group, group_created = Group.objects.get_or_create(name=instance.user_type)
        if group_created:
            group.permissions.add(*Permission.objects.filter(codename__in=permissions))
        instance.groups.add(group)


@receiver(post_save, sender=Tenant)
def assign_tenant_group(sender, instance, created, **kwargs):
    assign_group(instance, created, [])


@receiver(post_save, sender=Landlord)
def assign_landlord_group(sender, instance, created, **kwargs):
    assign_group(instance, created, [])


@receiver(post_save, sender=Admin)
def assign_admin_group(sender, instance, created, **kwargs):
    assign_group(instance, created, [])
