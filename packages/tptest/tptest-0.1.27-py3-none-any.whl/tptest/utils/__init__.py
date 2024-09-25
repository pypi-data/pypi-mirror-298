import ssl
from .config_loader import load_config
from .spinner import SpinnerThread

config = load_config()
spinner_thread = SpinnerThread('')
ssl_context = ssl._create_unverified_context()
