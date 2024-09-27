import asyncclick as click
import websockets
import json
import asyncio
from ..utils import load_config, ssl_context
from ..utils.disconnect import disconnect


# ANSI color codes for terminal
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

config = load_config()


# Function to start a single test
async def get_job_data(websocket, job_id):
    """
    Handles the JSON response received from the WebSocket connection.

    Args:
        response (str): The JSON response string received from the WebSocket.

    Returns:
        str: The job ID extracted from the JSON response.
    """
    await websocket.send(json.dumps(
        {
            'action': 'batchJobStatus',
            'jobId': job_id,
        }
    ))
    response = await websocket.recv()

    # Handle the response and extract the job_id
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print("Failed to parse response as JSON")
        return None


def print_colored_status(task):
    """
    Prints the status of a task with appropriate coloring.

    Args:
        task (dict): A dictionary representing the task details.
    """
    status = task.get('status', 'UNKNOWN')
    contact_id = task.get('contact_id')

    # Color-code the output based on the status
    if status == "PASS":
        color = COLOR_GREEN
    elif status == "FAIL":
        color = COLOR_RED
    else:
        color = COLOR_BLUE  # For STARTED, SYS_FAIL, or others

    # Print the task information with colored status
    print(f"Contact ID: {contact_id} - Status: {color}{status}{COLOR_RESET}")


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


async def do(websocket, job_id):
    data = await get_job_data(websocket, job_id)

    if data is None:
        print("No valid data returned.")
        return

    # Extract the body from the response (if present)
    body = data.get('body')
    if body:
        try:
            json_body = json.loads(body)

            # Extract the 'message' from the response (if present)
            message = json_body.get('message')
            if message:
                total_tests = len(message)
                passed_tests = 0
                failed_tests = 0

                # Track whether all statuses are final (either PASS or FAIL)
                all_final = True

                for task in message:
                    # Print each task's status with appropriate color
                    print_colored_status(task)

                    status = task.get('status')
                    if status == "PASS":
                        passed_tests += 1
                    elif status == "FAIL":
                        failed_tests += 1

                # Use all() to check if all tasks have a final status (PASS or FAIL)
                all_final = all(task.get('status') in ["PASS", "FAIL"] for task in message)

                # Check if we need to stop (i.e., all statuses are either PASS or FAIL)
                if all_final:
                    print(f"\nFinal Status: {passed_tests}/{total_tests} tests PASSED.")
                    await disconnect(websocket)
                    return True  # Stop polling as all tests have completed
                else:
                    print(f"Current Status: {passed_tests}/{total_tests} tests PASSED.")
                    await disconnect(websocket)
                    return False  # Continue polling
            else:
                print("No 'message' found in response.")
        except json.JSONDecodeError:
            print(f"Failed to decode body as JSON: {body}")
    else:
        print("No data received yet.")


@click.command(name='check-api')
@click.option('--job-id', type=str, help='The UUID of the test to start.')
@click.option('--url', default=lambda: config.get('default_url'), callback=validate_start_test_options, help='The WebSocket URL to connect to.')
@click.option('--api-key', default=lambda: config.get('api_key'), callback=validate_start_test_options, help='The API key for authentication.')
async def check_api_cmd(job_id, url, api_key):
    try:
        async with websockets.connect(url, ssl=ssl_context, extra_headers={'x-api-key': api_key}) as websocket:
            while True:
                await do(websocket, job_id)
                await asyncio.sleep(2) 
    except websockets.exceptions.InvalidHandshake as e:
        print(f"Failed to establish WebSocket connection: {e}")
    except websockets.exceptions.ConnectionClosed as e:
        if e.code == 1000:
            print('Disconnected')
        else:
            print(f"WebSocket connection closed unexpectedly: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
