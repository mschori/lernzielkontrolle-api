from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from services.group_service import get_group_name_coach, get_group_name_student
from users.models import User


class Command(BaseCommand):
    """
    Class for management-command "set_default_entries".
    """
    help = 'Set default entries into the Database.'

    def handle(self, *args, **options):
        """
        Handle command.
        set default groups and users
        """
        try:
            print('Setting default groups and users.')
            Group.objects.bulk_create([
                Group(name=get_group_name_coach()),
                Group(name=get_group_name_student())
            ])

            User.objects.bulk_create([
                User(
                    email='max.mustermann@coach.com',
                    firstname='Max',
                    lastname='Mustermann'
                ),
                User(
                    email='hulda.musterfrau@coach.com',
                    firstname='Hulda',
                    lastname='Musterfrau'
                ),
                User(
                    email='martin.knecht@student.com',
                    firstname='Martin',
                    lastname='Knecht'
                ),
                User(
                    email='larissa.brunner@student.com',
                    firstname='Larissa',
                    lastname='Brunner'
                ),
            ])

            print('Setting groups for default users.')
            for user in User.objects.filter(email__in=['max.mustermann@coach.com', 'hulda.musterfrau@coach.com']):
                user.groups.add(Group.objects.get(name=get_group_name_coach()))
                user.save()

            for user in User.objects.filter(email__in=['martin.knecht@student.com', 'larissa.brunner@student.com']):
                user.groups.add(Group.objects.get(name=get_group_name_student()))
                user.save()
            print('Default entries set successfully.')
        except Exception as e:
            print('Error:', e)
            return
