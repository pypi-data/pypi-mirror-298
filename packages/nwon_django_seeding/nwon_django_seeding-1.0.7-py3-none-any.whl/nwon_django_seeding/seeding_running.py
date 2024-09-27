"""
Not exactly a solution we want to use for disabling our validation in the context of
seeding.

Despite some effort I could not make it work in any other way 😔
"""

from os import environ, getenv

KEY = "SEEDING_RUNNING"
VALUE_IS_RUNNING = "yes"


def set_seeding_is_running() -> None:
    """Set seeding is running to True"""

    environ[KEY] = VALUE_IS_RUNNING


def set_seeding_is_not_running() -> None:
    """Set seeding is running to False"""

    if KEY in environ:
        del environ[KEY]


def is_seeding_running() -> bool:
    """Is a seeding operation ongoing?"""

    return getenv(KEY) == VALUE_IS_RUNNING
