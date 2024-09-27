import concurrent.futures
from os import path
from typing import Callable, List, Optional, Type, Union

from django.db.models import Model
from django.db.models.base import ModelBase
from nwon_baseline import print_helper
from pydantic import BaseModel

from nwon_django_seeding.actions.write_database_seeds import write_database_seeds
from nwon_django_seeding.nwon_django_seeding_settings import NWON_DJANGO_SEED_SETTINGS
from nwon_django_seeding.typings import ModelSeed, SeedSet


class SeedParameters(BaseModel):
    model: Union[Type[ModelBase], Type[Model]]
    path_to_write: str
    post_json_processing: Optional[Callable[[str], None]]


def write_database_seed_sets(
    environment: str,
    seed_sets: List[SeedSet],
    print_debug=False,
    only_write_for_models: Optional[List[Type[Model]]] = None,
):
    """
    Write JSON files for a list of seed sets.

    We write them in parallel.
    """

    parameters = __prepare_parameters_for_parallel_execution(
        environment, seed_sets, only_write_for_models
    )

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(
            __write_seeds_parallel, parameters, [print_debug] * len(parameters)
        )


def __prepare_parameters_for_parallel_execution(
    environment: str,
    seed_sets: List[SeedSet],
    only_write_for_models: Optional[List[Type[Model]]] = None,
) -> List[SeedParameters]:
    """
    Prepare the parameters for parallel execution.

    They are returned as a list of tuples with:
     - the model
     - the path to write the file
     - optionally a function for post processing the JSON file
    """
    directories = NWON_DJANGO_SEED_SETTINGS.directories_for_environment(environment)
    default_seed_index = 1
    environment_seed_index = 1

    parameters: List[SeedParameters] = []

    for seed_set in seed_sets:
        directory = (
            directories.default_directory
            if seed_set.is_default_seed
            else directories.environment_directory
        )

        for model_seed in seed_set.models:
            file_name_prefix = (
                default_seed_index
                if seed_set.is_default_seed
                else environment_seed_index
            )

            if seed_set.is_default_seed:
                default_seed_index += 1
            else:
                environment_seed_index += 1

            if isinstance(model_seed, ModelSeed):
                post_json_processing = model_seed.post_json_processing
                django_model = model_seed.model
            else:
                post_json_processing = None
                django_model = model_seed

            # If we only want to write specific models, we skip the others
            if only_write_for_models and django_model not in only_write_for_models:
                continue

            app_name = __app_name_for_model(django_model)
            prefix = f"{file_name_prefix:03d}"
            model_name = __model_name(django_model)

            if app_name != NWON_DJANGO_SEED_SETTINGS.default_app_name:
                file_name = f"{prefix}_{model_name}__{app_name}.json"
            else:
                file_name = f"{prefix}_{model_name}.json"

            path_to_write = path.join(directory, file_name)

            parameters.append(
                SeedParameters(
                    model=django_model,
                    path_to_write=path_to_write,
                    post_json_processing=post_json_processing,
                )
            )

    return parameters


def __write_seeds_parallel(parameters: SeedParameters, print_debug: bool):
    write_database_seeds(
        parameters.path_to_write,
        __model_identifiers([parameters.model]),
        parameters.post_json_processing,
    )

    if print_debug:
        print_helper.print_green(f"Created seed file in {parameters.path_to_write}")


def __model_name(model: Union[Type[Model], Type[ModelBase]]):
    return model.__name__.lower()


def __app_name_for_model(model: Union[Type[Model], Type[ModelBase]]) -> str:
    if issubclass(model, Model):
        return model._meta.app_label

    return NWON_DJANGO_SEED_SETTINGS.default_app_name


def __model_identifier(model: Union[Type[Model], Type[ModelBase]]):
    app_name = __app_name_for_model(model)

    return (
        f"{app_name}.{model._meta.model_name}"
        if issubclass(model, Model)
        else f"{app_name}.{model.__name__.lower()}"
    )


def __model_identifiers(models: List[Union[Type[Model], Type[ModelBase]]]):
    return [__model_identifier(model) for model in models]
