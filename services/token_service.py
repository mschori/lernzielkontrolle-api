from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


def get_tokens_for_user(user: User) -> dict:
    """
    Get jwt-access and -refresh-token for given user.
    :param user: user-object
    :return: dict with access- and refresh-token.
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
