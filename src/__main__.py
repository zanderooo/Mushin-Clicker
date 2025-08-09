import sys
import os
import json
import customtkinter as ctk

if sys.platform == "win32":
    import winsound

from pynput import mouse, keyboard
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from automation_engine import AutomationEngine
from gui import App

CONFIG_FILE = "mushin_config.json"

class MainApplication:
    def __init__(self):
        self.engine = AutomationEngine(self.update_status, self.on_engine_stop)
        
        self.hotkeys = {
            'toggle_app': keyboard.Key.f6,
            'toggle_app_str': 'F6',
            'toggle_record': keyboard.Key.f7,
            'toggle_record_str': 'F7',
        }
        
        # We only store the initial state here. The Tkinter variable is in the App.
        self.initial_sound_state = True

        self.app = App(self)
        
        self.is_picking_location = False
        self.is_binding_hotkey = False
        self.hotkey_to_bind = None
        
        self.global_listener = keyboard.Listener(on_press=self.on_global_key_press)
        self.global_listener.start()
        self.mouse_listener = None

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_settings()

    def on_closing(self):
        self.save_settings()
        self.app.destroy()

    def _play_sound(self, sound_type: str):
        # Query the variable from the App object
        if not self.app.sound_enabled.get() or sys.platform != "win32":
            return
        
        sounds = {
            'start': (800, 100),
            'stop': (600, 100),
            'record': (1200, 75)
        }
        if sound_type in sounds:
            freq, dur = sounds[sound_type]
            try:
                winsound.Beep(freq, dur)
            except Exception as e:
                print(f"Error playing sound: {e}")

    def on_engine_stop(self):
        self.app.after(0, self.app.set_active_state, False, '')

    def on_global_key_press(self, key):
        if self.is_binding_hotkey:
            self._set_new_hotkey(key)
            return

        if key == self.hotkeys['toggle_app']:
            if self.engine.is_running.is_set():
                self.engine.stop()
                self._play_sound('stop')
            else:
                self.start_app()
        elif key == self.hotkeys['toggle_record']:
            self.toggle_recording()

    def start_app(self, mode=None):
        active_tab = self.app.tab_view.get()
        current_mode = 'macro' if active_tab == "Macro Recorder" else 'clicker'
        
        if mode is None:
            mode = current_mode
        
        self.app.set_active_state(True, mode)
        self._play_sound('start')

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
            self._play_sound('stop')
            if self.mouse_listener and self.mouse_listener.is_alive():
                self.mouse_listener.stop()
            self.app.update_macro_display(self.engine.macro_events)
        else:
            self._play_sound('record')
            self.engine.start_recording()
            self.mouse_listener = mouse.Listener(on_click=self._on_macro_click)
            self.mouse_listener.start()

    def _on_macro_click(self, x, y, button, pressed):
        if pressed and self.engine.is_recording:
            self.engine._record_event('click', pos=(x, y), button_name=button.name, presses=1)
    
    def on_cps_change(self, value):
        self.app.update_cps_label(value)

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
            return False

    def start_hotkey_binding(self, key_name):
        self.is_binding_hotkey = True
        self.hotkey_to_bind = key_name
        self.update_status(f"Press any key to set as the new hotkey...")

    def _set_new_hotkey(self, key):
        try: key_str = key.char
        except AttributeError: key_str = f"{key}".replace("Key.", "")
        
        self.hotkeys[self.hotkey_to_bind] = key
        self.hotkeys[f"{self.hotkey_to_bind}_str"] = key_str
        self.app.update_hotkey_label(self.hotkey_to_bind, key_str)
        
        self.is_binding_hotkey = False
        self.hotkey_to_bind = None
        self.update_status("Hotkey updated.")

    def update_status(self, text):
        self.app.status_label.configure(text=text)

    def save_settings(self):
        settings = {
            'cps': self.app.cps_slider.get(),
            'click_limit': self.app.limit_entry.get(),
            'mouse_button': self.app.button_combobox.get(),
            'position_mode': self.app.pos_mode_segmented.get(),
            'target_position': self.engine.target_position,
            'macro_events': self.engine.macro_events,
            'sound_enabled': self.app.sound_enabled.get()
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(settings, f, indent=4)
            print("INFO: Settings saved.")
        except Exception as e:
            print(f"ERROR: Could not save settings. {e}")

    def load_settings(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    settings = json.load(f)
                
                self.app.cps_slider.set(settings.get('cps', 10))
                self.app.update_cps_label(settings.get('cps', 10))
                self.app.limit_entry.insert(0, settings.get('click_limit', ''))
                self.app.button_combobox.set(settings.get('mouse_button', 'Left'))
                self.on_button_change(self.app.button_combobox.get())
                
                pos_mode = settings.get('position_mode', 'Cursor')
                self.app.pos_mode_segmented.set(pos_mode)
                self.on_position_mode_change(pos_mode)
                if pos_mode == 'Fixed' and settings.get('target_position'):
                    self.engine.target_position = tuple(settings['target_position'])
                    x, y = self.engine.target_position
                    self.app.pos_label.configure(text=f"X:{x} Y:{y}")

                self.engine.macro_events = settings.get('macro_events', [])
                self.app.update_macro_display(self.engine.macro_events)
                
                self.app.sound_enabled.set(settings.get('sound_enabled', True))

                print("INFO: Settings loaded.")
        except Exception as e:
            print(f"ERROR: Could not load settings. {e}")

    def run(self):
        self.app.mainloop()
        self.global_listener.stop()
        if self.mouse_listener and self.mouse_listener.is_alive():
            self.mouse_listener.stop()

if __name__ == "__main__":
    main_app = MainApplication()
    main_app.run()