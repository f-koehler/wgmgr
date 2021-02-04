from pathlib import Path
from typing import Any

import yaml


def load_yaml_file(path: Path) -> Any:
    with open(path, "r") as fptr:
        try:
            from yaml import CLoader

            return yaml.load(fptr, Loader=CLoader)
        except ImportError:
            from yaml import Loader

            return yaml.load(fptr, Loader=Loader)


def generate_yaml(data: Any) -> str:
    try:
        from yaml import CDumper

        return yaml.dump(data, Dumper=CDumper)
    except ImportError:
        from yaml import Dumper

        return yaml.dump(data, Dumper=Dumper)


def write_yaml_file(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as fptr:
        fptr.write(generate_yaml(data))
