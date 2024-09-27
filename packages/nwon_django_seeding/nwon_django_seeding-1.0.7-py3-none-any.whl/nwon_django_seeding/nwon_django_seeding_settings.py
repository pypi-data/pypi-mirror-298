from django.conf import settings
from pydantic import ValidationError

from nwon_django_seeding.typings import (
    NWONDjangoSeedingSettings,
)


def set_settings() -> NWONDjangoSeedingSettings:
    """
    Parse Settings from Django settings
    """

    if not hasattr(settings, "NWON_DJANGO_SEEDING"):
        raise Exception("You need to set NWON_DJANGO_SEEDING in your Django settings")

    if isinstance(settings.NWON_DJANGO_SEEDING, NWONDjangoSeedingSettings):
        return settings.NWON_DJANGO_SEEDING

    if not isinstance(settings.NWON_DJANGO_SEEDING, dict):
        raise Exception(
            "The NWON_DJANGO_SEEDING settings need to be of type dict or NWONDjangoSeedingSettings"
        )

    try:
        return NWONDjangoSeedingSettings.model_validate(settings.NWON_DJANGO_SEEDING)
    except ValidationError as exception:
        raise Exception(
            f"Could not parse the NWON_DJANGO settings: {str(exception)}"
        ) from exception


NWON_DJANGO_SEED_SETTINGS = set_settings()
"""
Settings used withing the NWON-django-seeding package
"""


__all__ = ["NWON_DJANGO_SEED_SETTINGS"]
