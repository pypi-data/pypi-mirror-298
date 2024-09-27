import json
from typing import List

from nwon_django_seeding.typings import DjangoSeed


def load_seeds_from_file(json_path: str) -> List[DjangoSeed]:
    return_value: List[DjangoSeed] = []

    with open(json_path, "r", encoding="utf-8") as file:
        json_string = file.read()
        json_data = json.loads(json_string)

        if isinstance(json_data, list):
            for data in json_data:
                return_value.append(DjangoSeed.model_validate(data))

    return return_value
