import os
from time import sleep

import firebase_admin
from firebase_admin import auth, credentials

from custom_exceptions.firebase_exceptions import FirebaseUserNotFoundException, FirebaseTokenNotFoundException
from users.models import User

firebase_admin.initialize_app(credentials.Certificate({
    'type': os.getenv('FIREBASE_TYPE'),
    'project_id': os.getenv('FIREBASE_PROJECT_ID'),
    'private_key_id': os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    'private_key': os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    'client_email': os.getenv('FIREBASE_CLIENT_EMAIL'),
    'client_id': os.getenv('FIREBASE_CLIENT_ID'),
    'auth_uri': os.getenv('FIREBASE_AUTH_URI'),
    'token_uri': os.getenv('FIREBASE_TOKEN_URI'),
    'auth_provider_x509_cert_url': os.getenv('FIREBASE_AUTH_PROVIDER'),
    'client_x509_cert_url': os.getenv('FIREBASE_CLIENT_CERT_URL')
}))


def get_user_infos_with_id_token(id_token: str) -> auth.UserRecord:
    """
    Get user infos from firebase with given id-token.
    :param id_token: firebase id-token
    :return: user-record from firebase
    """
    if not id_token:
        raise FirebaseTokenNotFoundException
    try:
        sleep(1)
        decoded_user = auth.verify_id_token(id_token)
        return auth.get_user(decoded_user['user_id'])
    except (auth.UserNotFoundError, ValueError, Exception) as e:
        print(e)
        raise FirebaseUserNotFoundException


def revoke_refresh_token(user: User) -> bool:
    """
    Revoke refresh-token for given user in firebase.
    :param user: user to revoke refresh-token
    :return: bool
    """
    try:
        auth.revoke_refresh_tokens(user.uid)
        return True
    except Exception as e:
        print(e)
        return False
