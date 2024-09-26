# Create a new error class called ParameterError that inherits from the built-in ValueError class.
from typing import Any


class RetrieveMatchError(Exception):
    def __init__(self, message: str = None, *args: Any):
        if message :
            self.message = message
            super().__init__(self.message, *args)

class RetrieveOddsError(Exception):
    def __init__(self, message: str = None, *args: Any):
        if message :
            self.message = message
            super().__init__(self.message, *args)
