import sys
import json
import os
import time
from .disconnect import disconnect
from .get_websocket import get_websocket

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

is_github_actions = os.environ.get('GITHUB_ACTIONS', 'false').lower() == 'true'


# Function to get the status of a single test
async def waiter(websocket, job_id, spinner, job_type):
    # Start the spinner thread
    spinner.start()

    try:

        if job_type and job_type == 'single':
            # Send a request to listen for test status updates
            await websocket.send(json.dumps({'action': 'jobStatus', 'jobId': job_id, 'jobType': job_type}))

            # Listen for test status updates
            while True:
                status_update = await websocket.recv()
                json_response = json.loads(status_update)
                json_body = json.loads(json_response.get('body', '{}'))

                message = json_body.get('message', None)

                if message:
                    date = message.split(' | ')[0]
                    status = message.split(' | ')[1]
                    status_with_colour = f"{RED}failed{RESET}" if status == 'failed' else f"{GREEN}passed{RESET}"
                    msg_string = message.split(' | ')[2]

                errorMessage = json_body.get('errorMessage', None)

                if errorMessage:
                    sys.stdout.write('\r' + ' ' * 80 + '\r')  # Clear the line
                    print(f'Error: {errorMessage}')
                    await disconnect(get_websocket())
                    sys.exit(1)
                else:
                    if status == 'failed':
                        sys.stdout.write('\r' + ' ' * 80 + '\r')  # Clear the line
                        print(f"{date} | {status_with_colour} | {msg_string}")
                        await disconnect(get_websocket())
                        sys.exit(1)
                    if status == 'complete':
                        sys.stdout.write('\r' + ' ' * 80 + '\r')  # Clear the line
                        print(f"{date} | {status_with_colour} | {msg_string}")
                        await disconnect(get_websocket())
                        break
                    else:
                        if not is_github_actions:
                            sys.stdout.write('\r' + ' ' * 80 + '\r')  # Clear the line
                            print(f"{date} | {status_with_colour} | {msg_string}")
                        else:
                            print(f"{date} | {status_with_colour} | {msg_string}")
        elif job_type and job_type == 'batch':
            for i in range(1000):
                data = await websocket.send(json.dumps({'action': 'batchJobStatus', 'jobId': job_id, 'jobType': job_type}))
                print(data)
                time.sleep(1)
        else:
            print('No Type passed')
    finally:
        spinner.stop()
        spinner.join()
