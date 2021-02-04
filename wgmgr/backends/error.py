class BackendError(Exception):
    pass


class BackendOptionError(BackendError):
    pass


class MissingBackendOptionError(Exception):
    def __init__(self, option_name: str):
        self.option_name = option_name
        self.message = f"Missing backend option: {option_name}"