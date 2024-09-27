import threading
import itertools
import time
import sys
import os


class SpinnerThread(threading.Thread):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.spinner_chars = itertools.cycle(['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'])
        self.running = True
        self.start_time = time.time()
        self.is_github_actions = os.environ.get('GITHUB_ACTIONS', 'false').lower() == 'true'

    def run(self):
        if self.is_github_actions:
            print('Supress Test Progress Messages while running in CI.')
        while self.running:
            elapsed_time = int(time.time() - self.start_time)
            if not self.is_github_actions:
                sys.stdout.write(f'\r{next(self.spinner_chars)} Executing Test (Elapsed Time: {elapsed_time}s)')
                sys.stdout.flush()
            else:
                sys.stdout.flush()
            time.sleep(0.1)

    def stop(self):
        self.running = False
        sys.stdout.write('\r \r')  # Clear the spinner line
        sys.stdout.flush()
