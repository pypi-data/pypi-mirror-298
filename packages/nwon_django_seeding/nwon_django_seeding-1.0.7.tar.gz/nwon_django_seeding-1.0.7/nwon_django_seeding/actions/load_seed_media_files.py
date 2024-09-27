import re
from os.path import basename, exists
from typing import List

from django.core.files.base import File as DjangoFile
from django.db.models.signals import post_delete, post_save, pre_save
from nwon_baseline import print_helper
from nwon_baseline.directory_helper import file_paths_in_directory
from nwon_django_toolbox.signals import disable_signals, enable_signals

from nwon_django_seeding.nwon_django_seeding_settings import NWON_DJANGO_SEED_SETTINGS


def load_seed_media_files(environment: str):
    print_helper.print_green(f"Loading seed media files for {environment} environment")

    disable_signals([post_delete, post_save, pre_save])

    for file_folder in NWON_DJANGO_SEED_SETTINGS.file_directories_for_environment(
        environment
    ):
        if exists(file_folder.path):
            paths = file_paths_in_directory(file_folder.path)
            for path in paths:
                file_name = basename(path)

                if file_name == ".keep":
                    continue

                primary_keys: List[str] = re.findall(r"(\d+)", file_name)

                if len(primary_keys) < 1:
                    raise Exception(
                        f"Path {path} does not contain a number in order to tie a "
                        + "file to an instance of {file_folder.model}"
                    )

                primary_key = primary_keys[0]

                try:
                    instance = file_folder.model.objects.get(pk=primary_key)
                except file_folder.model.DoesNotExist:
                    print_helper.print_error(
                        f"Could not find {file_folder.model} with "
                        + f"{primary_key} for seeding {path}"
                    )
                    continue

                with open(path, "rb") as file:
                    setattr(
                        instance, file_folder.file_key, DjangoFile(file, name=file_name)
                    )
                    instance.save()

                    class_name = instance.__class__.__name__
                    print_helper.print_blue(
                        f"Loaded media file from {path} to {class_name} "
                        + "with pk {instance.pk} for "
                    )
        else:
            print_helper.print_warning(
                f"Could not load seed files from {file_folder.path} "
                + "as the directory does not exist."
            )

    enable_signals([post_delete, post_save, pre_save])
