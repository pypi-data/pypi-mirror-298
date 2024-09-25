from .configure import configure_cmd
from .start_test import start_test_cmd
from .start_batch_test import start_batch_test_cmd


def register_commands(cli):
    cli.add_command(start_test_cmd)
    cli.add_command(configure_cmd)
    cli.add_command(start_batch_test_cmd)