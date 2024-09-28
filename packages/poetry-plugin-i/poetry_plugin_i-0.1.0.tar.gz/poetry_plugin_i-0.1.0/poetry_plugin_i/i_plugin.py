from typing import List, Type

from poetry.console.commands.command import Command
from poetry.console.commands.install import InstallCommand
from poetry.plugins.application_plugin import ApplicationPlugin


class ICommand(InstallCommand):
    name = "i"


class CustomPlugin(ApplicationPlugin):
    @property
    def commands(self) -> List[Type[Command]]:
        return [ICommand]
