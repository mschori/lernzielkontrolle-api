class FirebaseUserNotFoundException(Exception):
    """
    Exception raised when a user tries to login with credentials that do not exist.
    """
    message = 'Firebase user not found.'


class FirebaseTokenNotFoundException(Exception):
    """
    Exception raised when a user tries to login with an invalid firebase token.
    """
    message = 'Firebase token not found.'
