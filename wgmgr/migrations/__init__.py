from typing import Any, Callable


def load_migration(from_version: int) -> Callable[[dict[str, Any]], dict[str, Any]]:
    pass
