from typing import Callable, Dict, List, Optional, Type, Union

from django.db.models import Model
from django.db.models.base import ModelBase
from nwon_baseline.typings import AnyDict
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ModelFolderMapping(BaseModel):
    """Defines how the files for a model will be saved for usage in seeding"""

    model: Type[Model]
    path: str
    """ Path to the directory where the files gonna be saved """
    file_key: str
    """ Model field where the file is stored """


class SeedDirectories(BaseModel):
    default_directory: str
    environment_directory: str


class NWONDjangoSeedingSettings(BaseModel):
    disable_signals_before_seeding_model: Callable[[], List[Type[Model]]] = Field(
        description="Callable that returns all models for which signals should be disabled before seeding. Reenabled after seeding that model."
    )
    custom_seed_map: Callable[[], Dict[Type[Model], Dict[str, str]]] = Field(
        description="This function returns a map that configures our custom seeding logic for specific models. It maps a model class to a dictionary that contains the field names in the database and maps them to the field names in the seed file."
    )
    directories_for_environment: Callable[[str], SeedDirectories] = Field(
        description="A function taking the name on an environment and returning the "
        + "relevant seed directories"
    )
    file_directories_for_environment: Callable[[str], List[ModelFolderMapping]] = Field(
        description="A function taking the name on an environment and returning "
        + " a list of model folder mappings that defines which files we want to seed."
    )
    default_app_name: str = Field(description="The default app name for the seed files")

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel),
        populate_by_name=True,
        extra="forbid",
    )


class DjangoSeed(BaseModel):
    """This is the structure of the Django seed data."""

    model: str
    pk: int
    fields: AnyDict


class ModelSeed(BaseModel):
    """
    This is a model that should be seeded and needs some extra JSON post processing.

    This was necessary to cover seeds that have circular dependencies. This makes
    it possible to seed this model first without the reference to another model and
    only after creating the other model the full model with the relation.
    """

    model: Union[Type[Model], Type[ModelBase]]
    post_json_processing: Callable[[str], None]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class SeedSet(BaseModel):
    """
    A set of models that logically belong together. This is mainly used to group models.
    """

    models: List[Union[Type[Model], Type[ModelBase], ModelSeed]]
    is_default_seed: Optional[bool] = Field(default=False)
    """ If true this models will always be put in the default folder """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
