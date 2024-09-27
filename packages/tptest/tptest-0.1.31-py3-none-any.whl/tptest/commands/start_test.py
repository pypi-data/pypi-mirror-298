import asyncclick as click
import websockets
import json
from ..utils import load_config, ssl_context
from ..utils.waiter import waiter
from ..utils import spinner_thread

config = load_config()


# Function to start a single test
async def start_test(websocket, test_id, job_name, job_description):
    """
    Handles the JSON response received from the WebSocket connection.

    Args:
        response (str): The JSON response string received from the WebSocket.

    Returns:
        str: The job ID extracted from the JSON response.
    """
    await websocket.send(json.dumps(
        {
            'action': 'startTest',
            'testId': test_id,
            'jobName': job_name,
            'jobDescription': job_description,
        }
    ))

    # Handle the response and extract the job_id
    response = await websocket.recv()
    json_response = json.loads(response)
    json_body = json.loads(json_response.get('body', '{}'))
    job_id = json_body.get('job_id')

    return job_id


def validate_start_test_options(ctx, param, value):
    # Check if the parameter being validated is the --url option
    if param.name == 'url':
        if not value:
            raise click.BadParameter('--url is required and cannot be empty', ctx=ctx)

    # Check if the parameter being validated is the --api-key option
    elif param.name == 'api_key':
        if not value:
            raise click.BadParameter('--api-key is required and cannot be empty', ctx=ctx)

    # Check if the parameter being validated is the --job-name option
    elif param.name == 'job_name':
        if not value:
            raise click.BadParameter('--job-name is required and cannot be empty', ctx=ctx)

    # Check if the parameter being validated is the --job-description option
    elif param.name == 'job_description':
        if not value:
            raise click.BadParameter('--job-description is required and cannot be empty', ctx=ctx)

    # Check if the parameter being validated is the --test-ids option
    elif param.name == 'test_id':
        if not value:
            raise click.BadParameter('--test-id is required and cannot be empty', ctx=ctx)

    # If all validations pass, return the value
    return value


@click.command(name='start-test')
@click.option('--test-id', callback=validate_start_test_options, type=str, help='The UUID of the test to start.')
@click.option('--job-name', callback=validate_start_test_options, help='Add a Job Name for easier reporing.')
@click.option('--job-description', callback=validate_start_test_options, help='Provide a description for the job.')
@click.option('--url', default=lambda: config.get('default_url'), callback=validate_start_test_options, help='The WebSocket URL to connect to.')
@click.option('--api-key', default=lambda: config.get('api_key'), callback=validate_start_test_options, help='The API key for authentication.')
async def start_test_cmd(test_id, url, api_key, job_name, job_description):
    try:
        async with websockets.connect(url, ssl=ssl_context, extra_headers={'x-api-key': api_key}) as websocket:
            job_id = await start_test(websocket, test_id, job_name, job_description)
            print(f'Started test with job ID: {job_id}')
            await waiter(websocket, job_id, spinner_thread, 'single')
    except websockets.exceptions.InvalidHandshake as e:
        print(f"Failed to establish WebSocket connection: {e}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"WebSocket connection closed unexpectedly: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
