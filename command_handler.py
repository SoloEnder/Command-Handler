import logging
from exceptions import CommandNotFoundError, WrongArgTypeError, ArgumentsCountError

logging.basicConfig(level=10)

class Command:
    """
    The model for the command object used by the CommandHandler

    Attribute:
        - command_name (str): the name of the command (given in the __init__)
        - command_args (keyword): the args need for the command => arg_name='arg_type'
            - argument_types = 'str'=>string, 'int'=>integer, 'true'=>True, 'false'=>False, 'none'=>None
        - command_func (func object): the associeted function

    Methods:
        - exec_command: call the associeted command (by the attribute 'func')
    """

    def __init__(self, command_name: str, command_func, **kw):
        self.command_name = command_name
        self.command_func = command_func
        self.command_args = kw

    def exec_command(self, given_args):
        self.command_func(given_args)

class CommandHandler:
    """
    A command handler

    Attributes:
        - commands (list): a list of Command() objects, représent the available commands

    Methods:
        - add_command: method for add a new command to the list of commands
        - exec_command: execute the command
        - find_command: check if a command exist in the command database (list commmands)
    """

    def __init__(self):
        self.commands = []

    
    def add_command(self, command_name: str, command_func, **kw):
        """
        Create a new Command() object

        Args:
            - command_name (str): the name for the new command
            - command_func (function object): the function associated to the new command
            - kw (keyword): the args need for the command => arg_name='arg_type'
                - argument_types = 'str'=>string, 'int'=>integer, 'true'=>True, 'false'=>False, 'none'=>None
        """
        command = Command(command_name, command_func, kw=kw)
        self.commands.append(command)
        logging.debug(f"Command_adder: Command named '{command_name}' associeted with '{command_func}' added\n")

    def exec_command(self, given_name: str, given_args: list):
        """
        Find and execute a command

        Args:
            - given_name (str): the name of the requested command

        Raise:
            - CommandNotFoundError : if there is no match for the requested command in the commands list

        """
        command_found = self.find_command(given_name)
        command_args = command_found.command_args
        self.check_args_len(command_args, given_args)
        converted_args = self.convert_given_args(command_args, given_args)
        command_found.exec_command(converted_args)

    def find_command(self, given_name: str):
        """
        Search the command name in the command database

        Args:
            - given_name (str): the name of the searched command

        Returns:
            - bool: False if the given_name not found
            - command object: the object of the command (class) if the command found
        """

        for command in self.commands:

            if command.command_name == given_name:
                return command
            
        raise CommandNotFoundError(given_name)
    
    def check_args_len(self, command_args: dict, given_args: list) -> bool:
        """
        Check if the given number argument match with the need argument number

        Args:
            - command_args (dict): the arguments need by the command
            - given_args (list): the arguments given by the user

        Returns:
            - bool: True if the argument number match, False otherwise
        """

        if len(given_args) == len(command_args["kw"]):
            return True
        
        else:
            raise ArgumentsCountError(command_args)
        
    def convert_given_args(self, command_args: dict, given_args_list: list) -> dict:
        command_args = command_args["kw"]
        """
        Convert the given args into the type need by the command function

        Args:
            - command_args (dict): the needed type of arguments
            - given_args (list): the argument given by the user

        Returns:
            - dict: the command arguments name in keys, and the converted given arguments in value
        """
        args_type = {
            "str":str,
            "int":int,
            "float":float,
            }
        index = -1

        given_args_dict = {}

        for arg_name, excepted_type in command_args.items():
            index += 1
            given_arg = given_args_list[index]

            if given_arg.startswith("'") and given_arg.endswith("'"):
                given_arg.replace("'", "")
                given_args_dict[arg_name] = given_arg
                continue

            if given_arg.startswith('"') and given_arg.endswith('"'):
                given_arg.replace('"', '')
                given_args_dict[arg_name] = given_arg
                continue
            
            type_exception = ["true", "false", "none"]

            try:

                if given_arg.lower() not in type_exception:
                    given_arg = args_type[excepted_type](given_arg)

                else:
                    given_arg = given_arg.lower()

                    if given_arg == "true":
                        given_arg = True

                    elif given_arg == "false":
                        given_arg = False

                    elif given_arg == "none":
                        given_arg = None

            except ValueError:

                raise WrongArgTypeError(given_arg, excepted_type)

            else:
                given_args_dict[arg_name] = given_arg

        return given_args_dict