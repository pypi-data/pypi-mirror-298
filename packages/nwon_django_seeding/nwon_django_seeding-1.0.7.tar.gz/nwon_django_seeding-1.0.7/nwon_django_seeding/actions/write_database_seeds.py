import subprocess
from typing import Callable, List, Optional


def write_database_seeds(
    target_file: str,
    model_or_apps_to_dump: List[str],
    post_json_processing: Optional[Callable[[str], None]] = None,
):
    """
    Write seed to file via console output as passing the proper
    arguments was not possible.
    """

    arguments: List[str] = model_or_apps_to_dump + [
        "--natural-foreign",
        "--indent",
        "2",
    ]

    with open(target_file, "w", encoding="utf-8") as outfile:
        subprocess.run(["python", "manage.py", "dumpdata"] + arguments, stdout=outfile)

    # Post process the JSON file when defined
    if post_json_processing is not None:
        post_json_processing(target_file)
