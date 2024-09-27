import os
from typing import Optional, Tuple, Type

from django.apps import apps
from django.db.models import Model

from nwon_django_seeding.nwon_django_seeding_settings import NWON_DJANGO_SEED_SETTINGS


def parse_info_from_seed_file_name(
    file_path: str, default_app_label: Optional[str] = None
) -> Tuple[str, str, Type[Model]]:
    """
    Get some information the file name of a seed file.

    The file name structure is:
    <index>_<model_name>.json or <index>_<model_name>__<app_name>.json

    If the app_name is not specified the default_app_label is used.
    """

    if not default_app_label:
        default_app_label = NWON_DJANGO_SEED_SETTINGS.default_app_name

    base_name = os.path.basename(file_path)
    base_name_without_suffix = base_name.split(".")[0]
    model_name = (
        "_".join(base_name_without_suffix.split("_")[1:])
        if "_" in base_name_without_suffix
        else base_name_without_suffix
    )

    if "__" in model_name:
        splitted_model_name = model_name.split("__")
        model_name = splitted_model_name[0]
        app_name_to_use = splitted_model_name[1]
    else:
        app_name_to_use = default_app_label

    model_class = apps.get_model(app_name_to_use.lower(), model_name)

    return (model_name.lower(), app_name_to_use.lower(), model_class)
