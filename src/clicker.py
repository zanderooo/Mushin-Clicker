import time
import threading
from pynput.mouse import Button, Controller

class Clicker:
    def __init__(self):
        self.mouse = Controller()
        self.clicking_thread = None
        self.is_clicking = threading.Event() # We use threading.Event for safely stopping the thread
        
        self.cps = 10.0  # Default clicks per second
        self.mouse_button = Button.left

    def _click_loop(self):
        """The loop that performs clicks in a separate thread."""
        # Calculate delay only when CPS changes, not every loop
        try:
            delay = 1.0 / self.cps
        except ZeroDivisionError:
            delay = 1.0

        while self.is_clicking.is_set():
            self.mouse.click(self.mouse_button, 1)
            # Recalculate delay inside the loop if CPS can change dynamically
            try:
                delay = 1.0 / self.cps
            except ZeroDivisionError:
                delay = 1.0
            time.sleep(delay)

    def start_clicking(self):
        """Starts the clicking process if not already active."""
        if not self.is_clicking.is_set():
            self.is_clicking.set()
            self.clicking_thread = threading.Thread(target=self._click_loop, daemon=True)
            self.clicking_thread.start()
            print("INFO: Clicking started.")

    def stop_clicking(self):
        """Stops the clicking process."""
        if self.is_clicking.is_set():
            self.is_clicking.clear()
            # We wait for the thread to finish, with a timeout just in case
            if self.clicking_thread:
                self.clicking_thread.join(timeout=0.2)
            print("INFO: Clicking stopped.")

    def set_cps(self, cps):
        """Sets the new clicks per second value."""
        if cps > 0:
            self.cps = cps
            print(f"INFO: CPS set to {self.cps}")

    def set_mouse_button(self, button_name: str):
        """Sets the mouse button for clicking."""
        button_map = {
            "Left": Button.left,
            "Right": Button.right,
            "Middle": Button.middle
        }
        self.mouse_button = button_map.get(button_name, Button.left)
        print(f"INFO: Mouse button set to {self.mouse_button}")