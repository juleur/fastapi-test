class EmailNotFoundError(Exception):
    pass


class UsernameNotFoundError(Exception):
    pass


class WrongCredentialsError(Exception):
    pass


class PasswordTooShortError(Exception):
    pass


class DogNotFound(Exception):
    pass
