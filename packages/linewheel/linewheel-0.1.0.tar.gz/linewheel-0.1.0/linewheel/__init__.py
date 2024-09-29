from __future__ import annotations
import cmd
from typing import List
from linewheel.command import Command, Function, Subprocess


class Cmd(cmd.Cmd):

    def __init__(self) -> None:
        super().__init__()

    def get_names(self):
        # This returns a list of all methods of the class
        # including the dynamically added
        return dir(self)

    def preloop(self):
        return self.do_help(None)


class CommandLineInterface:

    default_prompt = '> '

    default_commands = [
        Command(name='exit', fn=lambda arg: True),
    ]

    def __init__(self, builder: Builder) -> None:
        self._cmd = Cmd()
        self._cmd.prompt = builder._prompt
        for command in CommandLineInterface.default_commands:
            setattr(self._cmd, f'do_{command.name}', command.fn)
        for command in builder._commands:
            setattr(self._cmd, f'do_{command.name}', command.fn)

    @staticmethod
    def builder(prompt: str = default_prompt) -> Builder:
        return CommandLineInterface.Builder(prompt)
    
    def loop(self):
        self._cmd.cmdloop()

    class Builder:

        def __init__(self, prompt: str) -> None:
            self._prompt = prompt
            self._commands: List[Command] = []

        def __enter__(self) -> CommandLineInterface.Builder:
            return self

        def __exit__(self, exc_type, exc_value, traceback) -> None:
            pass

        def command(self, command: Command) -> None:
            self._commands.append(command)

        def build(self) -> CommandLineInterface:
            return CommandLineInterface(self)
