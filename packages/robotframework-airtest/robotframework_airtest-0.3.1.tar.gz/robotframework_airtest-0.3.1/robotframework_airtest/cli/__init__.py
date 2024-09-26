from collections import OrderedDict
import click
from . import template
from . import vmg


class NaturalOrderGroup(click.Group):
    """Command group trying to list subcommands in the order they were added.
    Example use::

        @click.group(cls=NaturalOrderGroup)

    If passing dict of commands from other sources, ensure they are of type
    OrderedDict and properly ordered, otherwise order of them will be random
    and newly added will come to the end.
    """

    def __init__(self, name=None, commands=None, **attrs):
        if commands is None:
            commands = OrderedDict()
        elif not isinstance(commands, OrderedDict):
            commands = OrderedDict(commands)
        click.Group.__init__(self, name=name, commands=commands, **attrs)

    def list_commands(self, ctx):
        """List command names as they are in commands dict.

        If the dict is OrderedDict, it will preserve the order commands
        were added.
        """
        return self.commands.keys()


@click.group(cls=NaturalOrderGroup)
def main():
    """
    ================================================================
                    Airtest For RobotFramework
    ================================================================

    """
    pass


template.setup(main)
vmg.setup(main)
