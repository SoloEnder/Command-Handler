
from typing import Literal

class CommandCallHandler:

    def __init__(self, func, command_call: str, moment: Literal["before", "after"]):
        self.func = func
        self.command_call = command_call
        self.moment = moment