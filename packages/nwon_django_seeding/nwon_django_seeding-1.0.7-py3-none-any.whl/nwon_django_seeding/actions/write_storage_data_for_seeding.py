import sys
from os import mkdir
from os.path import basename, exists, join

from botocore.exceptions import EndpointConnectionError
from nwon_baseline import directory_helper, print_helper

from nwon_django_seeding.nwon_django_seeding_settings import NWON_DJANGO_SEED_SETTINGS


def write_storage_data_for_seeding(environment: str):
    """
    Copy files stored in the storage for all defined models into a folder. From there
     we take them during seeding.
    """

    print_helper.print_green(f"Writing seed files for {environment} environment")

    for mapped in NWON_DJANGO_SEED_SETTINGS.file_directories_for_environment(
        environment
    ):
        clean_directory = False

        if not exists(mapped.path):
            mkdir(mapped.path)
        else:
            clean_directory = True

        for model_instance in mapped.model.objects.all():
            file = getattr(model_instance, mapped.file_key)

            if file:
                try:
                    file_content = file.read()

                    """
                    We delay cleaning directory until we are sure that we have a
                    connection to the S3
                    """
                    if clean_directory:
                        directory_helper.clean_directory(mapped.path)
                        clean_directory = False

                    file_name: str = basename(file.name)
                    target_file_name = (
                        file_name
                        if file_name.startswith(str(model_instance.pk))
                        else f"{model_instance.pk}_{file_name}"
                    )

                    target_file_path = join(mapped.path, target_file_name)

                    with open(target_file_path, "wb+") as target_file:
                        target_file.write(file_content)

                    print_helper.print_blue(
                        f"Wrote file for {mapped.model.__name__} with pk "
                        + f"{model_instance.pk} to {target_file_path}."
                    )
                except EndpointConnectionError:
                    print_helper.print_error("Could not connect to S3. Exiting 💣")
                    sys.exit()
                except FileNotFoundError:
                    print_helper.print_error(
                        f"Could not read file {file.name} in "
                        + f"{mapped.model.__name__} with pk "
                        + str(model_instance.pk)
                    )
