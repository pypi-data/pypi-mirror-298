import abc
import subprocess
from typing import Callable


@staticmethod
def executable(fn) -> Callable[[str], bool]:
    def wrapper(arg) -> bool:
        fn(arg)
        print()
        return False
    return wrapper


class Command(abc.ABC):

    def __init__(self, name: str, fn: Callable) -> None:
        self.name = name
        self.fn = fn


class Function(Command):

    def __init__(self, name: str, fn: Callable) -> None:
        super().__init__(name, executable(fn))


class Subprocess(Command):

    def __init__(self, name: str, command: str) -> None:
        fn = lambda arg: subprocess.run(command.split())
        super().__init__(name, executable(fn))
