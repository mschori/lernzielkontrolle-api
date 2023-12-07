from firebase_admin import auth

from custom_exceptions.user_exceptions import EmailAlreadyExistsException
from users.models import User


def get_or_create_user(firebase_user_record: auth.UserRecord) -> User:
    """
    Get a user based on given user-infos.
    If no use can be found then create a new user with given user-infos.
    :param firebase_user_record: user-record from firebase-auth
    :return: user-object
    :exception EmailAlreadyExistsException: if email already exists
    """
    user = User.objects.filter(firebase_uid=firebase_user_record.uid).first()
    if not user and User.objects.filter(email=firebase_user_record.email).exists():
        raise EmailAlreadyExistsException
    elif not user:
        user = User.objects.create(
            firebase_uid=firebase_user_record.uid,
            email=firebase_user_record.email,
            firstname=firebase_user_record.display_name.split(' ')[0] if firebase_user_record.display_name else '',
            lastname=firebase_user_record.display_name.split(' ')[1] if firebase_user_record.display_name else '',
            is_active=True
        )
    return user
