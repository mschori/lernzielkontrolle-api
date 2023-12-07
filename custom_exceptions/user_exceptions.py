class EmailAlreadyExistsException(Exception):
    """
    Exception raised when a user tries to register with an email that already exists.
    """
    message = 'Email already exists.'
