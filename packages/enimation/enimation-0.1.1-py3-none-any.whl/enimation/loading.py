import threading
import time
import functools

class CustomLoading:
    def __init__(self, animation_function=None, interval=0.1):
        """Initialize CustomLoading with a user-defined animation function."""
        self.animation_function = animation_function or self.default_animation
        self.interval = interval
        self.stop_event = threading.Event()

    def default_animation(self):
        """Default animation logic (can be overridden)."""
        frames = ['-', '\\', '|', '/']
        while not self.stop_event.is_set():
            for frame in frames:
                print(f'\rLoading {frame}', end='', flush=True)
                time.sleep(self.interval)

    def start(self):
        """Start the loading animation in a separate thread."""
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.animation_function)
        self.thread.start()

    def stop(self):
        """Stop the loading animation."""
        self.stop_event.set()
        self.thread.join()
        print()  # Move to the next line after loading

def loading(custom_loading_instance=None):
    """Decorator to add loading animation to a function."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use the provided custom loading instance or default
            loader = custom_loading_instance or CustomLoading()
            loader.start()

            # Execute the actual function
            result = func(*args, **kwargs)

            # Stop the loading animation
            loader.stop()
            return result
        return wrapper
    return decorator
