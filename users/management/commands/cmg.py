from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from sender.models import Sender
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        group_manager = Group.objects.create(name='Manager')
        content_type_1 = ContentType.objects.get_for_model(Sender)
        content_type_2 = ContentType.objects.get_for_model(User)

        permission_sender_view, __ = Permission.objects.get_or_create(codename='view_sender',
                                                                      content_type=content_type_1)
        group_manager.permissions.add(permission_sender_view)

        permission_sender_set_disabled, __ = Permission.objects.get_or_create(codename='set_disabled',
                                                                              content_type=content_type_1)
        group_manager.permissions.add(permission_sender_set_disabled)

        permission_users_view, __ = Permission.objects.get_or_create(codename='view_user',
                                                                     content_type=content_type_2)
        group_manager.permissions.add(permission_users_view)

        permission_users_set_disabled, __ = Permission.objects.get_or_create(codename='set_disabled',
                                                                             content_type=content_type_2)
        group_manager.permissions.add(permission_users_set_disabled)
