
class UnknownArgument(ValueError):

    def __init__(self, arg):
        super().__init__()
        self.arg = arg

    def __str__(self):
        return f"Unknown keyword argument '{self.arg}'"
    
class CommandExists(ValueError):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"A command with the name '{self.name}' already exists in this handler"
    
class CommandNotFound(ValueError):

    def __init__(self, name: str|None=None, index: int|None=None):
        super().__init__()
        self.name = name
        self.index = index


    def __str__(self):

        if self.name:
            return f"Unknown command name '{self.name}'"
        
        elif self.index or type(self.index) == int:
            return f"No command found in the command list of this hanlder at the given index '{self.index}'"

