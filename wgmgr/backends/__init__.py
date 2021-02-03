from enum import Enum
from .ansible_group import AnsibleGroup


class Backends(str, Enum):
    ansible_group = "ansible_group"


def get_backend_class(backend: Backends):
    if backend == Backends.ansible_group:
        return AnsibleGroup
