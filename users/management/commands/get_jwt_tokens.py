from django.core.management.base import BaseCommand

from services.token_service import get_tokens_for_user
from users.models import User


class Command(BaseCommand):
    """
    Class for management-command "get_jwt_tokens".
    """
    help = 'Get the JWT-Token for a user.'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email')

    def handle(self, *args, **options):
        """
        Handle command.
        """
        try:
            user = User.objects.get(email=options['email'])
            tokens = get_tokens_for_user(user)
            print('Access-Token:', tokens['access'])
            print('Refresh-Token:', tokens['refresh'])
        except User.DoesNotExist:
            print('User does not exist.')
            return
