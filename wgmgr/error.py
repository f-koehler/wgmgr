class DuplicatePeerError(Exception):
    def __init__(self, name: str):
        super().__init__(f"peer already exists: {name}")


class UnknownPeerError(Exception):
    def __init__(self, name: str):
        super().__init__(f"unknown peer: {name}")


class FreeAddressError(Exception):
    def __init__(self, protocol: str):
        super().__init__(f"no free {protocol} address")


class ConfigVersionError(Exception):
    def __init__(self, version: int, current_version: int):
        super().__init__(
            f"config version {version} is newer than supported version "
            f"{current_version}"
        )


class MissingMigration(Exception):
    def __init__(self, from_version: int, to_version: int):
        super().__init__(
            f"missing migration for config version {from_version} -> {to_version}"
        )
