from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers.
    """

    def create_user(self, email: str, password=None, uid: str = 'not defined', **extra_fields):
        """
        Create and save a User with the given email, password and uid.
        :param email: email address
        :param password: password
        :param uid: firebase-uid
        :param extra_fields: extra fields
        :return: user-object
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), uid=uid, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, uid: str = 'not defined', **extra_fields):
        """
        Create and save a SuperUser with the given email, password and uid.
        :param email: email address
        :param password: password
        :param uid: firebase-uid
        :param extra_fields: extra fields
        :return: user-object
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.create_user(email, password, uid, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user
