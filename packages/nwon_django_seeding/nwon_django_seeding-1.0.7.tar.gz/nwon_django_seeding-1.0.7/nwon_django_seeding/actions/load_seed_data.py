import copy
from typing import Any, Dict, Optional

from django.core.management import call_command
from django.db import transaction
from django.db.models.signals import post_save
from nwon_baseline import directory_helper, print_helper
from nwon_django_toolbox.signals import disable_signals, enable_signals

from nwon_django_seeding.helper.load_seeds_from_file import load_seeds_from_file
from nwon_django_seeding.helper.parse_info_from_seed_file_name import (
    parse_info_from_seed_file_name,
)
from nwon_django_seeding.nwon_django_seeding_settings import NWON_DJANGO_SEED_SETTINGS


def load_seed_data(environment: str, app_name: Optional[str] = None):
    """
    Loads seed files for a specific environment.

    We always load the default seed files first and then the environment specific ones.
    """

    directories = NWON_DJANGO_SEED_SETTINGS.directories_for_environment(environment)

    """ Disable signals for the following models in order to prevent
    race conditions between seeding and signals """
    disable_signals_for_models = (
        NWON_DJANGO_SEED_SETTINGS.disable_signals_before_seeding_model()
    )

    for directory in [directories.default_directory, directories.environment_directory]:
        print_helper.print_green(f"Loading seed files from {directory}")

        file_paths = directory_helper.file_paths_in_directory(directory, ["json"])
        file_paths.sort()

        for file in file_paths:
            print_helper.print_green(f"Loading seed from {file}")

            # Make sure to commit all pending transactions before loading the seed
            if transaction.get_autocommit():
                transaction.commit()

            model_name, app_name_to_use, _ = parse_info_from_seed_file_name(
                file, app_name
            )
            disable_signal = model_name in [
                m.__name__.lower() for m in disable_signals_for_models
            ]

            if disable_signal:
                disable_signals([post_save])

            __load_seed_file(file, app_name_to_use)

            # Commit all pending transactions stemming from the seed file
            if transaction.get_autocommit():
                transaction.commit()

            # reenable signals if they were disabled
            if disable_signal:
                enable_signals([post_save])


def __load_seed_file(file: str, app: str):
    """
    For most seed files we just use the builtin Django mechanism to load the data.

    But for some models we create/update the data manually by using get_or_create in
    order to prevent constraint clashes.
    """

    _, app_name_to_use, model_class = parse_info_from_seed_file_name(file, app)

    map = NWON_DJANGO_SEED_SETTINGS.custom_seed_map()
    if model_class in map:
        seed_model_map = map[model_class]
        seeds = load_seeds_from_file(file)

        for seed in seeds:
            fields = copy.deepcopy(seed.fields)

            for key_in_seed_file in seed_model_map.values():
                del fields[key_in_seed_file]

            find_by_keys: Dict[str, Any] = {}
            for database_field_name, key_in_seed_file in seed_model_map.items():
                find_by_keys = {
                    **find_by_keys,
                    database_field_name: seed.fields[key_in_seed_file],
                }

            model_class.objects.update_or_create(**find_by_keys, defaults={**fields})
    else:
        call_command(
            "loaddata",
            file,
            app_label=app_name_to_use,
        )
