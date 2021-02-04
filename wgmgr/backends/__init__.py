from enum import Enum
from typing import Dict, List, Optional, Union

from .ansible_group import AnsibleGroup
from .base import Backend
from .error import UnknownBackendError


class Backends(str, Enum):
    ansible_group = "ansible_group"


def convert_backend_options(options: Optional[List[str]]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    if not options:
        return result

    for option in options:
        key, value = option.split(":", 1)
        result[key] = value

    return result


def create_backend(
    backend: Backends, options: Union[Optional[List[str]], Dict[str, str]]
) -> Backend:
    if not isinstance(options, dict):
        options = convert_backend_options(options)

    if backend == Backends.ansible_group:
        return AnsibleGroup.from_options(options)

    raise UnknownBackendError(str(backend))
