from .configure import configure_cmd
from .start_test import start_test_cmd
from .start_batch_test import start_batch_test_cmd
from .check_api import check_api_cmd

"""
This module is responsible for registering the commands available in the CLI.
"""

"""
Registers the commands available in the CLI.
:param cli: The Click command group object.
"""
# pylint: disable=unused-argument
# pylint: disable=redefined-builtin


def register_commands(cli):
    cli.add_command(start_test_cmd)
    cli.add_command(configure_cmd)
    cli.add_command(start_batch_test_cmd)
    cli.add_command(check_api_cmd)


"""
Registers the commands available in the CLI.
:param cli: The Click command group object.
"""
