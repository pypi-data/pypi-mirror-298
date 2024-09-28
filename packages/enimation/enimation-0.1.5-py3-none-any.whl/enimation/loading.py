import threading
import time
import functools
import inspect  # Missing import
from . import motions as motions

def get_func(module):
    function_list = []
    # Get all functions defined in the module
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        function_list.append(name)
    return function_list

class CustomLoading:
    def __init__(self, custom=None, interval=0.1):
        """Initialize CustomLoading with a user-defined animation function."""
        self.animation_function = custom or self.default_animation
        self.interval = interval
        self.stop_event = threading.Event()

    def default_animation(self, stop_event):
        """Default animation logic (can be overridden)."""
        frames = ['-', '\\', '|', '/']
        while not stop_event.is_set():
            for frame in frames:
                print(f'\rLoading {frame}', end='', flush=True)
                time.sleep(self.interval)

    def start(self):
        """Start the loading animation in a separate thread."""
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.animation_function, args=(self.stop_event,))
        self.thread.start()

    def stop(self):
        """Stop the loading animation."""
        self.stop_event.set()
        self.thread.join()
        print()  # Move to the next line after loading

def list_animations():
    """List available animation functions from the motions module."""
    print("Available Pre Animation Functions (list format):")
    print(get_func(motions))

def loading(custom=None):
    """Decorator to add loading animation to a function."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use the provided custom loading instance or default
            loader = CustomLoading(custom=custom)  # Fixed this line
            loader.start()

            # Execute the actual function
            result = func(*args, **kwargs)

            # Stop the loading animation
            loader.stop()
            return result
        return wrapper
    return decorator 
