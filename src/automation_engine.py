import time
import threading
from pynput import mouse, keyboard

class AutomationEngine:
    def __init__(self, update_status_callback):
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.update_status_callback = update_status_callback

        # General state
        self.is_running = threading.Event()
        self.main_thread = None

        # Clicker settings
        self.cps = 10.0
        self.mouse_button = mouse.Button.left
        self.click_limit = 0  # 0 for infinite
        self.target_position = None  # None for current cursor position

        # Macro settings
        self.macro_events = []
        self.is_recording = False
        self._last_time = None

    def _record_event(self, event_type, **kwargs):
        if not self.is_recording:
            return

        current_time = time.time()
        delay = current_time - self._last_time if self._last_time else 0
        self._last_time = current_time
        
        event = {'type': event_type, 'delay': delay}
        event.update(kwargs)
        self.macro_events.append(event)
        print(f"Recorded: {event}")

    def start_recording(self):
        if not self.is_recording:
            self.macro_events = []
            self.is_recording = True
            self._last_time = time.time()
            self.update_status_callback("Recording... Press Stop Hotkey to finish.")
            print("INFO: Recording started.")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.update_status_callback(f"Recording stopped. {len(self.macro_events)} events saved.")
            print("INFO: Recording stopped.")
    
    def clear_macro(self):
        self.macro_events = []
        self.update_status_callback("Macro cleared.")

    def _playback_loop(self):
        self.update_status_callback("Playing macro...")
        for event in self.macro_events:
            if not self.is_running.is_set():
                break
            
            time.sleep(event['delay'])
            
            if event['type'] == 'click':
                self.mouse_controller.position = event['pos']
                self.mouse_controller.click(event['button'], event['presses'])
            elif event['type'] == 'move':
                self.mouse_controller.position = event['pos']
        
        if self.is_running.is_set(): # If loop finished naturally
            self.stop()
            self.update_status_callback("Macro finished.")

    def _click_loop(self):
        delay = 1.0 / self.cps if self.cps > 0 else 1.0
        clicks_done = 0
        
        self.update_status_callback(f"Clicking at {self.cps:.1f} CPS...")

        while self.is_running.is_set():
            if self.target_position:
                self.mouse_controller.position = self.target_position
            
            self.mouse_controller.click(self.mouse_button, 1)
            clicks_done += 1
            
            if self.click_limit > 0 and clicks_done >= self.click_limit:
                break
                
            time.sleep(delay)
        
        if self.is_running.is_set(): # If loop finished naturally
            self.stop()
            self.update_status_callback(f"Finished {clicks_done} clicks.")

    def start(self, mode='clicker'):
        if not self.is_running.is_set():
            self.is_running.set()
            loop_target = self._click_loop if mode == 'clicker' else self._playback_loop
            self.main_thread = threading.Thread(target=loop_target, daemon=True)
            self.main_thread.start()
            print(f"INFO: {mode.capitalize()} started.")

    def stop(self):
        if self.is_running.is_set():
            self.is_running.clear()
            if self.main_thread:
                self.main_thread.join(timeout=0.2)
            self.update_status_callback("Idle.")
            print("INFO: Process stopped.")