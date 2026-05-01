
from typing import Literal
import logging
import dill
import exceptions
from command import Command
from command_call_handler import CommandCallHandler


logging.basicConfig(level=logging.DEBUG, format="[{asctime}] - [{name}] - [{levelname}] : {msg}", style="{")

class CommandHandler:

    def __init__(self, commands: list|None=None):
        self.commands = commands if commands else []
        self.commands_calls_history = []
        self.commands_calls_handlers = []

    def add_command(self, name: str, func, *args):
        """
        Create a command and add it to the command list

        Args:
            - name (str): the name of the command (used for call it)
            - func: the function attached to the command (executed at every call of the command name)
            - args (tuple): the name of the arguments supported by the command function
        """

        if self.command_exists(name):
            raise exceptions.CommandExists(name)
        
        else:
            command_object = Command(name, func, *args)
            self.commands.append(command_object)
            logging.info("A command has been added")
            logging.debug(f"{name=}, {func=}, {args=}")

    def delete_command(self, name: str|None=None, index: int|None=None):
        """
        Delete a command object from the command list

        Args:
            - name (str) : the name of the command to delete
            - index (int): the index of the command to delete

        Raises:
            - CommandNotFound : if no command is found for the given name/index
        """

        if name:
            command_index = self.command_exists(name, get_index=True)

            if command_index or type(command_index) == int:
                del self.commands[command_index]

            else:
                raise exceptions.CommandNotFound(name=name)
        
        elif type(index) == int:

            try:
                del self.commands[index]
                print("deleted")

            except IndexError:
                raise exceptions.CommandNotFound(index=index)
            
    def edit_command(self, command_name:str|None=None, index: int|None=None, **kwargs):
        """
        Edit the attributes 'name', 'func' and 'args' of a Command instance

        Args:
            - name (str) : the name of the command to edit
            - index (str): the index of the command to edit
            - kwargs (kwargs): the new value to set to the Command instance attributes
                - name (str): the new value of the attribue 'name'
                - func (function object): the new value for the attribue 'func'
                - args (tuple): the new value for the attribute 'args'

        Raises:
            - CommandNotFound : if no command is found for the given name/index

        """

        if command_name:
            command_object = self.get_command(command_name)

        elif index or index == 0:

            try:
                command_object = self.commands[index]

            except IndexError:
                raise exceptions.CommandNotFound(index=index)

        command_object.name = kwargs.get("name", command_object.name)
        command_object.func = kwargs.get("func", command_object.func)
        command_object.args = kwargs.get("args", command_object.args)

    def exec_command(self, command_name, check_args=True, **kwargs):
        logging.debug(f"{command_name=}")
        command_object = self.get_command(command_name)
        cmd_call_hander = None

        for cmd_call_hander in self.commands_calls_handlers:

            if cmd_call_hander.command_call == command_name:
                logging.info(f"A command call handler has been found for the command '{command_name}'")

                if cmd_call_hander.moment == "before":
                    cmd_call_hander.func()


        if self.check_args(kwargs.keys(), command_object.args):
            self.commands_calls_history.append(command_object.name)
            logging.debug(f"Function {command_object.func} associated with command {command_object.name} called")
            logging.info(f"Command '{command_object.name} called !'")
            command_object.func(**kwargs)

            if cmd_call_hander and cmd_call_hander.moment == "after":
                cmd_call_hander.func()


    def check_args(self, given_args, cmd_args: tuple):
        """
        Check if the keywords arguments given to a command are accepted by the command

        Args:
            given_args: the keywords arguments given to the command
            cmd_args (tuple): the keywords arguments accepted by the command

        Returns:
            True: if the given arguments match with the arguments accepted by the command

        Raises:
            - UnknownArgument : if an argument not handled by the command function
        """

        for given_arg in given_args:

            if not given_arg in cmd_args:
                raise exceptions.UnknownArgument(given_arg)

        return True
    
    def command_exists(self, name, get_index: bool=False):
        """
        Check if a given command name exists in the command list of the current handler

        Args:
            given_name (str): the given name
            get_index (bool): if setted to True, the function will return the index of the command found in the command list 

        Returns:
            True: if a command with this name exists
            False: if no command with this name is found
            Int: if get_index set to True
 
        """

        for index, cmd in enumerate(self.commands):

            if cmd.name == name:

                if get_index:
                    return index
                
                else:
                    return True

        else:
            return False
        
    def get_command(self, name: str):
        """
        Get and return a command object from the commands object list

        Args:
            - name (str): the name of the wanted command

        Returns:
            - command_object: the command object

        Raises:
            - CommandNotFound : if no command is found for the given name
        """
        command_index = self.command_exists(name, get_index=True)
        logging.debug(f"{command_index=}")

        if not command_index and not type(command_index) == int:
            raise exceptions.CommandNotFound(name=name)
        
        else:
            return self.commands[command_index]
        
    def add_call_handler(self, cmd_call_handler):
        logging.info("A new command calls handler has been added")
        self.commands_calls_handlers.append(cmd_call_handler)

def say(**kwargs):
    print(kwargs.get("text", "hello !"))

def on_say():
    print("Something has been say")

on_say_handler = CommandCallHandler(command_call="say", func=on_say, moment="after")
cmd_h = CommandHandler()
cmd_h.add_command("say", say, "text")
cmd_h.add_call_handler(on_say_handler)
cmd_h.exec_command("say")
