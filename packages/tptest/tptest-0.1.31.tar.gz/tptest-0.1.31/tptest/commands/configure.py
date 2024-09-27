import asyncclick as click
import json
import os


@click.command(name='configure', help='Configure the application with an API Key and WSS URL')
@click.option('--url', help='The WebSocket URL to connect to.')
@click.option('--api-key', help='The API key for authentication.')
@click.option('--show-config', is_flag=True, help='Display the current configuration.')
@click.option('--reset-config', is_flag=True, help='Reset the configuration.')
def configure_cmd(url=None, api_key=None, show_config=False, reset_config=False):
    config_data = {}

    # read the config file if it exists
    if show_config:
        config_file = os.path.join(os.path.expanduser('~'), '.tptest.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                print(f"\nCurrent configuration:\n\nAPI Key: {config_data['api_key']}\nWSS URL: {config_data['default_url']}\n\n")
                return
        else:
            print('No configuration found.')
            return

    # reset the config by deleting the file
    if reset_config:
        config_file = os.path.join(os.path.expanduser('~'), '.tptest.json')
        if os.path.exists(config_file):
            os.remove(config_file)
            print('Configuration reset successful.')
            return
        else:
            print('No configuration found.')
            return

    # Use the provided API key or prompt the user if not provided
    if api_key:
        config_data['api_key'] = api_key
    else:
        config_data['api_key'] = click.prompt('Enter your API key', hide_input=True)

    # Use the provided URL or prompt the user if not provided
    if url:
        config_data['default_url'] = url
    else:
        config_data['default_url'] = click.prompt('Enter the WebSocket URL', default='wss://your-wss-url')

    # Write the configuration data to a JSON file
    config_file = os.path.join(os.path.expanduser('~'), '.tptest.json')
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=4)

    print(f'Configuration saved to {config_file}')
