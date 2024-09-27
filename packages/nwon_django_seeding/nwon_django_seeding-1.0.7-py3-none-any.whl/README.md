# NWON Django seeding

A bunch of functions that you can use for creating seeds for your current application state and loading them.

This is build on top of Django fixtures. This package helps you handle database content and media files as well.

## Settings

The Django Seeding package can be configured using the Django settings. We expect the key `NWON_DJANGO_SEEDING` that holds a dictionary or a pydantic object of type [NWONDjangoSeedingSettings](./nwon_django_seeding/typings.py). The dictionary must be parsable by [NWONDjangoSeedingSettings](./nwon_django_seeding/typings.py). The keys mus be snake case or camel case.

For example like this

```python
def directories_for_environment(environment: str) -> SeedDirectories:
    return SeedDirectories(default_directory="", environment_directory="")

def file_seeds_for_environment(environment: str) -> List[ModelFolderMapping]:
    return []

def disable_seeding() -> List[Type[Model]]:
    return []    

def custom_seed_map() -> Dict[Type[Model], Dict[str, str]]:
    return {}        

NWON_DJANGO_SEEDING: NWONDjangoSeedingSettings = {
    disable_signals_before_seeding_model=disable_seeding,
    custom_seed_map=custom_seed_map,
    directories_for_environment=directories_for_environment,
    file_directories_for_environment=file_seeds_for_environment,
    default_app_name="nwon",
}
```
