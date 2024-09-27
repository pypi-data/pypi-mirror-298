from typing import Optional, Type

from django.db.models import Model
from nwon_baseline import directory_helper

from nwon_django_seeding.helper.parse_info_from_seed_file_name import (
    parse_info_from_seed_file_name,
)
from nwon_django_seeding.nwon_django_seeding_settings import NWON_DJANGO_SEED_SETTINGS


def file_for_model_class(
    model_class: Type[Model], environment: str, app_name: Optional[str] = None
) -> str | None:
    """
    Get the seed file path for a model class
    """

    if not app_name:
        app_name = NWON_DJANGO_SEED_SETTINGS.default_app_name

    directories = NWON_DJANGO_SEED_SETTINGS.directories_for_environment(environment)
    for directory in [directories.default_directory, directories.environment_directory]:
        file_paths = directory_helper.file_paths_in_directory(directory, ["json"])

        for file in file_paths:
            model_name, _, _ = parse_info_from_seed_file_name(file, app_name)
            if model_name == model_class.__name__.lower():
                return file

    return None
