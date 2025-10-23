
class CommandNotFoundError(Exception):

    def __init__(self, command_name):
        self.command_name = command_name
        super().__init__()

    def __str__(self):
        return f"Command '{self.command_name}' not found'"
    
class WrongArgTypeError(TypeError):

    def __init__(self, gave_arg, excepted_arg_type):
        super().__init__()
        self.gave_arg = gave_arg
        self.excepted_arg_type = excepted_arg_type

    def __str__(self):
        return f"Gave argument '{self.gave_arg}' has not the excepted type '{self.excepted_arg_type}' "

class ArgumentsCountError(TypeError):

    def __init__(self, excepted_args):
        super().__init__()
        self.excepted_args = excepted_args

    def __str__(self):
        return f"Arguments missing or too many : {[(f"<{excepted_arg}>") for excepted_arg in self.excepted_args["kw"].keys()]}"
