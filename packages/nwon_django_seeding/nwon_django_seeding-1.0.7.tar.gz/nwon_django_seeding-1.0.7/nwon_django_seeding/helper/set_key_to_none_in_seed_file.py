import json

from nwon_django_seeding.helper.load_seeds_from_file import load_seeds_from_file


def set_key_to_none_in_seed_file(json_path: str, key: str):
    """
    Sets a key to None (aka. null in JSON) in the given seed file.
    """

    return_value = []
    seeds = load_seeds_from_file(json_path)

    for seed in seeds:
        if key in seed.fields:
            seed.fields[key] = None

        return_value.append(seed.model_dump())

    with open(json_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(return_value, indent=2))
