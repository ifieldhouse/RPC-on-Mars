class UnavailableFunction(Exception):
    pass


class UnavailableLog(Exception):
    pass


class InvalidData(Exception):
    pass


class AnonymousUser(Exception):
    """Anonymous users can't write into logs or read their own."""


class AnonymousRecipient(Exception):
    """Anonymous users don't have logs."""


class AlreadyExistingName(Exception):
    """There can't be two users with the same name."""