import sys
import os
from pynput import mouse, keyboard

# Add the src folder to the path to ensure correct imports
# when running and when packaged by PyInstaller.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from automation_engine import AutomationEngine
from gui import App

class MainApplication:
    def __init__(self):
        self.engine = AutomationEngine(self.update_status)

        # Define hotkeys BEFORE creating the App instance that uses them
        self.hotkeys = {
            'toggle_app': keyboard.Key.f6,
            'toggle_app_str': 'F6',
            'toggle_record': keyboard.Key.f7,
            'toggle_record_str': 'F7',
        }
        
        # Now create the App, which can safely access the hotkeys dictionary
        self.app = App(self)
        
        self.is_picking_location = False
        self.is_binding_hotkey = False
        self.hotkey_to_bind = None
        
        self.global_listener = keyboard.Listener(on_press=self.on_global_key_press)
        self.global_listener.start()
        
        self.mouse_listener = None

    def on_global_key_press(self, key):
        if self.is_binding_hotkey:
            self._set_new_hotkey(key)
            return

        if key == self.hotkeys['toggle_app']:
            if self.engine.is_running.is_set():
                self.engine.stop()
            else:
                self.start_app()
        elif key == self.hotkeys['toggle_record']:
            self.toggle_recording()

    def start_app(self, mode=None):
        if mode is None:
            # Determine mode from active tab
            active_tab = self.app.tab_view.get()
            mode = 'macro' if active_tab == "Macro Recorder" else 'clicker'

        if mode == 'clicker':
            self.engine.cps = float(self.app.cps_slider.get())
            try:
                limit = int(self.app.limit_entry.get())
                self.engine.click_limit = limit if limit > 0 else 0
            except (ValueError, TypeError):
                self.engine.click_limit = 0
        
        self.engine.start(mode)

    def toggle_recording(self):
        if self.engine.is_recording:
            self.engine.stop_recording()
            if self.mouse_listener and self.mouse_listener.is_alive():
                self.mouse_listener.stop()
            self.app.update_macro_display(self.engine.macro_events)
        else:
            self.engine.start_recording()
            self.mouse_listener = mouse.Listener(on_click=self._on_macro_click, on_move=self._on_macro_move)
            self.mouse_listener.start()

    def _on_macro_click(self, x, y, button, pressed):
        if pressed and self.engine.is_recording:
            self.engine._record_event('click', pos=(x,y), button=button, presses=1)
    
    def _on_macro_move(self, x, y):
        # This can be very noisy, maybe add a toggle for it in the future
        pass 

    def on_cps_change(self, value):
        self.app.update_cps_label(value)
        # We don't need to call self.engine.set_cps here, as it's set on Start

    def on_button_change(self, choice):
        button_map = {"Left": mouse.Button.left, "Right": mouse.Button.right, "Middle": mouse.Button.middle}
        self.engine.mouse_button = button_map.get(choice)

    def on_position_mode_change(self, value):
        if value == "Fixed":
            self.app.pick_location_btn.configure(state="normal")
        else:
            self.app.pick_location_btn.configure(state="disabled")
            self.engine.target_position = None
            self.app.pos_label.configure(text="X:--- Y:---")

    def start_picking_location(self):
        self.is_picking_location = True
        self.update_status("Click anywhere on the screen to set position.")
        self.mouse_listener = mouse.Listener(on_click=self._on_pick_location)
        self.mouse_listener.start()

    def _on_pick_location(self, x, y, button, pressed):
        if pressed and self.is_picking_location:
            self.engine.target_position = (x, y)
            self.app.pos_label.configure(text=f"X:{x} Y:{y}")
            self.is_picking_location = False
            self.update_status("Position set.")
            return False # Stop the listener

    def start_hotkey_binding(self, key_name):
        self.is_binding_hotkey = True
        self.hotkey_to_bind = key_name
        self.update_status(f"Press any key to set as the new hotkey...")

    def _set_new_hotkey(self, key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = f"{key}".replace("Key.", "")
        
        self.hotkeys[self.hotkey_to_bind] = key
        self.hotkeys[f"{self.hotkey_to_bind}_str"] = key_str
        self.app.update_hotkey_label(self.hotkey_to_bind, key_str)
        
        self.is_binding_hotkey = False
        self.hotkey_to_bind = None
        self.update_status("Hotkey updated.")

    def update_status(self, text):
        self.app.status_label.configure(text=text)

    def run(self):
        self.app.mainloop()
        self.global_listener.stop()
        if self.mouse_listener and self.mouse_listener.is_alive():
            self.mouse_listener.stop()

if __name__ == "__main__":
    main_app = MainApplication()
    main_app.run()