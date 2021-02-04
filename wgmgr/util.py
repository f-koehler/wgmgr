from pathlib import Path
from typing import Any

import yaml


def load_yaml_file(path: Path) -> Any:
    with open(path) as fptr:
        return yaml.safe_load(fptr)


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
