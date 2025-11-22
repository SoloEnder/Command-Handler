
class Command:

    def __init__(self, name, func, *args):
        self.name = name
        self.func = func
        self.args = args