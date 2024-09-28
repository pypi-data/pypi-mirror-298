
# enimation Package

**enimation** is a Python package that provides customizable loading animations for your console applications. It allows developers to easily integrate various loading indicators into their programs to enhance user experience.

## Installation

You can install the **enimation** package using pip:

```bash
pip install enimation
```
## Overview

The enimation package offers predefined animations and allows you to create custom animations. You can use these animations to indicate loading processes, improving the interactivity of your console applications.

# enimation Features

1. **Predefined Animations**  
   The package comes with multiple built-in loading animations:
   - Rotating Spinner
   - Dots Progress
   - Bouncing Ball
   - Wave Animation
   - Loading Bar with Percentage
   - Blinking Arrows
   - Scrolling Dashes
   - Growing Dots
   - Heartbeat Animation
   - Typing Effect

2. **Customizable Animations**  
   - Create your own custom loading animations by defining your own functions.
   - Custom animations can include dynamic loading text and other effects.
   - Easily integrate custom animations using the `CustomLoading` class.

3. **Stop Mechanism**  
   - All animations include a `stop_event` that ensures graceful termination when loading is complete.
   - No need to manually interrupt animations — they stop automatically when the task ends.

4. **Text Customization**  
   - You can customize the loading text for both predefined and custom animations. By default, the text is set to "Loading", but this can be changed to any string the user desires.

5. **Animation Timing Control**  
   - Control the speed of animations by adjusting the sleep intervals inside the animation logic.

6. **Lightweight and Easy to Integrate**  
   - The package is lightweight and can be easily integrated into any Python project. It's designed to work seamlessly without needing complex setup.

7. **Console Output Control**  
   - The animations utilize `sys.stdout.write()` and `sys.stdout.flush()` for smooth, non-newline output in the console.

8. **Versatile Use Cases**  
   - Perfect for CLI applications, long-running tasks, or any situation where you need to provide a visual loading indicator to the user.

# Usage

# Basic Usage decorator

Here's how to use the predefined animations in your Python project:

1. Import the Loading Decorator and Animation Functions:

```python
from enimation import loading
from enimation.motions import rotating_spinner
```

2. Create Your Function with a Loading Animation:

Use the `@loading` decorator to wrap your function, specifying the desired animation:

```python
@loading(custom=rotating_spinner)
def main():
    # Simulate a long-running task
    time.sleep(5)
    print("\nProcess complete!")
```

3. Run Your Program:

Call the main function to see the loading animation in action:

```python
if __name__ == "__main__":
    main()
```


## Advanced Usage decorator

For more advanced usage, you can customize the displayed text for each animation:

1. Using Custom Text:

To use custom text in your animation, modify the animation function call as follows:

```python
@loading(custom=lambda stop_event: rotating_spinner(stop_event, text="Processing..."))
def main():
    # Simulate a long-running task
    time.sleep(5)
    print("\nProcess complete!")
```


## Basic Usage Example

To use a predefined animation, follow this example:

```python
from enimation.loading import CustomLoading
import time

def main():
    # Create an instance of CustomLoading with a predefined animation
    loader = CustomLoading(custom='rotating_spinner')
    loader.start()  # Start the loading animation
    time.sleep(5)  # Simulate a long-running task
    loader.stop()   # Stop the loading animation
    print("\nTask complete!")  # Task completion message

if __name__ == "__main__":
    main()
```

## Creating Custom Animations

To create your own custom animation for the enimation package, follow these steps:

### Steps to Create a Custom Animation

1. Define a Function: Your custom animation should be defined as a function that accepts a stop_event parameter, which allows the animation to be stopped gracefully. You can also include an optional text parameter to customize the loading text.

```python
def custom_animation(stop_event, text="Loading"):
    # Animation logic goes here
```

2. Implement the Animation Logic: Inside your function, implement the logic for your animation using loops to update the console output.

### Example of a custom bouncing ball animation:

```python
import sys
import time

def custom_bouncing_ball(stop_event, text="Loading"):
    ball = ['.', 'o', 'O', 'o', '.']
    while not stop_event.is_set():
        for frame in ball:
            sys.stdout.write(f'\r{text} {frame}')
            sys.stdout.flush()
            time.sleep(0.3)  # Adjust the speed of the animation
```

3. Using the Custom Animation: To use your custom animation with the enimation loading mechanism, create an instance of CustomLoading, passing your custom animation function as the custom argument.

```python
from enimation.loading import CustomLoading
import time

def main():
    loader = CustomLoading(custom=custom_bouncing_ball)
    loader.start()  # Start the loading animation
    time.sleep(5)  # Simulate a long-running task
    loader.stop()   # Stop the loading animation
    print("\nTask complete!")  # Task completion message

if __name__ == "__main__":
    main()
```

## Required Components for Custom Animation

To ensure your custom animation works seamlessly with the enimation loading system, include the following:

`stop_event` Parameter: Use this parameter in your function to check whether the loading should continue.

Console Output: Use `sys.stdout.write()` and sys.stdout.flush() to update the console output without adding new lines.

Animation Logic: Implement the logic that defines how the animation behaves (e.g., changing frames, timing, and user-defined text).

Optional `text` Parameter: This parameter allows users to customize the loading message displayed alongside the animation.


## Example of a Complete Custom Animation Function

Here’s a complete example:

```python
import sys
import time
from enimation.loading import CustomLoading

def custom_wave_animation(stop_event, text="Loading"):
    wave = ['~', '~~', '~~~', '~~~~', '~~~', '~~', '~']
    while not stop_event.is_set():
        for frame in wave:
            sys.stdout.write(f'\r{text} {frame}')
            sys.stdout.flush()
            time.sleep(0.2)  # Adjust speed as needed

def main():
    loader = CustomLoading(custom=custom_wave_animation)
    loader.start()
    time.sleep(5)  # Simulate a long-running task
    loader.stop()
    print("\nTask complete!")

if __name__ == "__main__":
    main()
```

## Contributing

If you'd like to contribute to enimation, please fork the repository and submit a pull request. We welcome contributions of all kinds, including bug fixes, documentation improvements, and new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any inquiries or suggestions, feel free to reach out to:

hasan: hasanfq818@gmail.com

GitHub: [here](https://github.com/Kamanati/enimation)

# enimation
An animation function for python to higly customize you code with bueatyfull animation
