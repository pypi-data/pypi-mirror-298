import sys
import time

def rotating_spinner(stop_event, text="Loading"):
    """Spinner animation with customizable text."""
    spinner = ['|', '/', '-', '\\']
    while not stop_event.is_set():
        for frame in spinner:
            sys.stdout.write(f'\r{text} {frame}')
            sys.stdout.flush()
            time.sleep(0.1)

def dots_progress(stop_event, text="Loading"):
    """Dots loading animation with customizable text."""
    while not stop_event.is_set():
        for dots in range(1, 4):
            sys.stdout.write(f'\r{text}{"." * dots}   ')
            sys.stdout.flush()
            time.sleep(0.5)

def bouncing_ball(stop_event, text="Loading"):
    """Bouncing ball animation with customizable text."""
    ball = ['.', 'o', 'O', 'o', '.']
    while not stop_event.is_set():
        for frame in ball:
            sys.stdout.write(f'\r{text} {frame}')
            sys.stdout.flush()
            time.sleep(0.3)

def wave_animation(stop_event, text="Loading"):
    """Wave animation with customizable text."""
    wave = ['~', '~~', '~~~', '~~~~', '~~~', '~~', '~']
    while not stop_event.is_set():
        for frame in wave:
            sys.stdout.write(f'\r{text} {frame}')
            sys.stdout.flush()
            time.sleep(0.2)

def loading_bar_with_percentage(stop_event, text="Loading"):
    """Loading bar with percentage and customizable text."""
    total = 20
    while not stop_event.is_set():
        for i in range(total + 1):
            percent = (i / total) * 100
            bar = '=' * i + ' ' * (total - i)
            sys.stdout.write(f'\r{text} [{bar}] {percent:.0f}%')
            sys.stdout.flush()
            time.sleep(0.2)

def blinking_arrows(stop_event, text="Loading"):
    """Blinking arrows animation with customizable text."""
    arrows = ['←', '↑', '→', '↓']
    while not stop_event.is_set():
        for frame in arrows:
            sys.stdout.write(f'\r{text} {frame}')
            sys.stdout.flush()
            time.sleep(0.3)

def scrolling_dashes(stop_event, text="Loading"):
    """Scrolling dashes animation with customizable text."""
    while not stop_event.is_set():
        for i in range(1, 11):
            sys.stdout.write(f'\r{text} {"-" * i}{" " * (10 - i)}')
            sys.stdout.flush()
            time.sleep(0.1)

def growing_dots(stop_event, text="Loading"):
    """Growing dots animation with customizable text."""
    while not stop_event.is_set():
        for dots in range(1, 11):
            sys.stdout.write(f'\r{text}{"." * dots}   ')
            sys.stdout.flush()
            time.sleep(0.2)

def heartbeat_animation(stop_event, text="Loading"):
    """Heartbeat animation with customizable text."""
    heart = ['<3', '<33', '<333', '<33', '<3']
    while not stop_event.is_set():
        for frame in heart:
            sys.stdout.write(f'\r{text} {frame}')
            sys.stdout.flush()
            time.sleep(0.4)

def typing_effect(stop_event, text="Loading"):
    """Typing effect animation with customizable text."""
    while not stop_event.is_set():
        for i in range(len(text) + 1):
            sys.stdout.write(f'\r{text[:i]}')
            sys.stdout.flush()
            time.sleep(0.2)
        time.sleep(0.5) 
