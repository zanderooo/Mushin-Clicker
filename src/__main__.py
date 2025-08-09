import sys
import os
from pynput import keyboard

# Add the src folder to the path to ensure correct imports
# when running and when packaged by PyInstaller.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from clicker import Clicker
from gui import App

class MainApplication:
    def __init__(self):
        self.is_running = False  # Flag to track the clicking state
        self.hotkey = keyboard.Key.f6
        self.hotkey_str = "F6"

        self.clicker = Clicker()
        self.app = App(self.clicker, self.toggle_clicking, self.hotkey_str)
        
        # Initial button state setup
        self.app.update_button_state(self.is_running)
        
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def toggle_clicking(self):
        """Toggles the clicking state and updates the GUI."""
        self.is_running = not self.is_running
        if self.is_running:
            self.clicker.start_clicking()
        else:
            self.clicker.stop_clicking()
        
        # Update the GUI in the main thread to avoid issues
        self.app.after(0, self.app.update_button_state, self.is_running)

    def on_key_press(self, key):
        """Handles the hotkey press event."""
        if key == self.hotkey:
            self.toggle_clicking()

    def run(self):
        """Runs the main application loop."""
        self.app.mainloop()
        # Stop the key listener after the window is closed
        self.listener.stop()

if __name__ == "__main__":
    main_app = MainApplication()
    main_app.run()