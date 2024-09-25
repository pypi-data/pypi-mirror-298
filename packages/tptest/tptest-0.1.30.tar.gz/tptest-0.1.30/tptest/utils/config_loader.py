import os
import json
import sys


# Read a config file
def load_config():
    config_file = os.path.join(os.path.expanduser('~'), '.tptest.json')
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    # Check if the --help option is present in the command-line arguments
    if '--help' in sys.argv:
        # If --help is present, return the default configuration
        return {
            'api_key': '<your_api_key>',
            'default_url': 'https://your-default-url.com'
        }

    # if 'api_key' not in config:
    #     config['api_key'] = click.prompt('Please enter your API key', hide_input=True)

    # if 'default_url' not in config:
    #     config['default_url'] = click.prompt('Please enter the default URL', default='https://your-default-url.com')

    return config
