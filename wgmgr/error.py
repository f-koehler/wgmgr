class DuplicatePeerError(Exception):
    def __init__(self, name: str):
        super().__init__(f"peer already exists: {name}")


class UnknownPeerError(Exception):
    def __init__(self, name: str):
        super().__init__(f"unknown peer: {name}")


class FreeAddressError(Exception):
    def __init__(self, protocol: str):
        super().__init__(f"no free {protocol} address")
