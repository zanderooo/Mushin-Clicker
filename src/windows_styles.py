import customtkinter as ctk
import sys
import platform

# --- Constants for Theming ---
# Provide fallback fonts. The system will use the first one it finds.
FONT_FAMILY = ("JetBrains Mono", "Consolas", "Courier New", "monospace")
COLOR_PRIMARY = "#8A2BE2"  # Dark Violet / Purple
COLOR_SECONDARY = "#4B0082" # Indigo / Deeper Purple
COLOR_BACKGROUND = "#121212" # Almost Black
COLOR_FOREGROUND = "#1E1E1E" # Dark Gray for frames
COLOR_TEXT = "#E0E0E0" # Light Gray text

class App(ctk.CTk):
    def __init__(self, main_app_logic):
        super().__init__()
        self.logic = main_app_logic

        # --- Font Definition ---
        self.main_font = ctk.CTkFont(family=FONT_FAMILY[0], size=13) # Primary font
        self.mono_font = ctk.CTkFont(family=FONT_FAMILY[1], size=12) # Fallback for code
        self.small_font = ctk.CTkFont(family=FONT_FAMILY[0], size=11, slant="italic")
        self.value_font = ctk.CTkFont(family=FONT_FAMILY[0], size=13, weight="bold")

        # --- Window Configuration ---
        self.title("Mushin")
        self.geometry("450x550")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BACKGROUND) # Set a solid background color first

        # --- Apply Modern Windows Styles (More Robustly) ---
        self._apply_windows_styles()

        # --- Main Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Tab View Theming ---
        self.tab_view = ctk.CTkTabview(self, 
                                       fg_color="transparent",
                                       segmented_button_selected_color=COLOR_PRIMARY,
                                       segmented_button_unselected_color=COLOR_FOREGROUND,
                                       segmented_button_selected_hover_color=COLOR_SECONDARY)
        self.tab_view.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")
        self.tab_view.add("Auto Clicker")
        self.tab_view.add("Macro Recorder")
        self.tab_view._segmented_button.configure(font=self.main_font)

        # --- Status Bar ---
        self.status_label = ctk.CTkLabel(self, text="Idle.", font=self.small_font, text_color="#888")
        self.status_label.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")
        
        # --- Create Tabs ---
        self._create_clicker_tab(self.tab_view.tab("Auto Clicker"))
        self._create_macro_tab(self.tab_view.tab("Macro Recorder"))

    def _apply_windows_styles(self):
        """Applies modern visual styles to the window if on Windows 11."""
        if sys.platform != "win32" or int(platform.release()) < 10:
            return # Styles only work on Windows 10/11

        try:
            import pywinstyles
            # Try different styles for broader compatibility
            # 'mica' is often more reliable than 'acrylic'
            for style in ["mica", "acrylic", "transparent"]:
                try:
                    pywinstyles.apply_style(self, style)
                    print(f"INFO: Applied window style '{style}'.")
                    # Make the main frame background transparent to see the effect
                    self.configure(fg_color="transparent")
                    # Style the window bar
                    pywinstyles.change_header_color(self, color=COLOR_BACKGROUND)
                    pywinstyles.change_border_color(self, color=COLOR_SECONDARY)
                    return # Stop after the first successful style application
                except Exception as e:
                    print(f"WARNING: Failed to apply style '{style}': {e}")
            
            # If all styles fail, revert to a solid color
            print("WARNING: All transparency styles failed. Using solid background.")
            self.configure(fg_color=COLOR_BACKGROUND)
            
        except (ImportError, OSError) as e:
            print(f"WARNING: pywinstyles could not be used: {e}. Transparency disabled.")
            self.configure(fg_color=COLOR_BACKGROUND)

    def _create_styled_frame(self, parent):
        return ctk.CTkFrame(parent, fg_color="transparent")

    def _create_clicker_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        
        # --- CPS ---
        frame_cps = self._create_styled_frame(tab)
        frame_cps.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        frame_cps.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(frame_cps, text="Clicks Per Second", font=self.main_font).grid(row=0, column=0, sticky="w")
        self.cps_value_label = ctk.CTkLabel(frame_cps, text="10.0", font=self.value_font, text_color=COLOR_PRIMARY)
        self.cps_value_label.grid(row=0, column=2, sticky="e")
        self.cps_slider = ctk.CTkSlider(frame_cps, from_=1, to=100, command=self.logic.on_cps_change,
                                        button_color=COLOR_PRIMARY, progress_color=COLOR_SECONDARY)
        self.cps_slider.set(10)
        self.cps_slider.grid(row=1, column=0, columnspan=3, pady=(5,10), sticky="ew")

        # --- Click Limit ---
        frame_limit = self._create_styled_frame(tab)
        frame_limit.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        frame_limit.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(frame_limit, text="Click Count", font=self.main_font).grid(row=0, column=0, sticky="w")
        self.limit_entry = ctk.CTkEntry(frame_limit, placeholder_text="0 for infinite", font=self.main_font,
                                        border_color=COLOR_SECONDARY, fg_color=COLOR_FOREGROUND)
        self.limit_entry.grid(row=0, column=1, padx=10, sticky="ew")

        # --- Mouse Button ---
        frame_button = self._create_styled_frame(tab)
        frame_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(frame_button, text="Mouse Button", font=self.main_font).pack(side="left")
        self.button_combobox = ctk.CTkComboBox(frame_button, values=["Left", "Right", "Middle"], font=self.main_font,
                                               command=self.logic.on_button_change, dropdown_font=self.main_font,
                                               fg_color=COLOR_FOREGROUND, border_color=COLOR_SECONDARY,
                                               button_color=COLOR_SECONDARY, dropdown_fg_color=COLOR_BACKGROUND)
        self.button_combobox.pack(side="right", fill="x", expand=True, padx=(20,0))

        # --- Position ---
        frame_pos = self._create_styled_frame(tab)
        frame_pos.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(frame_pos, text="Click Position", font=self.main_font).pack(side="left")
        self.pos_mode_segmented = ctk.CTkSegmentedButton(frame_pos, values=["Cursor", "Fixed"], font=self.main_font,
                                                         command=self.logic.on_position_mode_change,
                                                         selected_color=COLOR_PRIMARY, unselected_color=COLOR_FOREGROUND,
                                                         selected_hover_color=COLOR_SECONDARY)
        self.pos_mode_segmented.set("Cursor")
        self.pos_mode_segmented.pack(side="left", padx=20)
        self.pick_location_btn = ctk.CTkButton(frame_pos, text="Pick", width=60, state="disabled", font=self.main_font,
                                               command=self.logic.start_picking_location, fg_color=COLOR_SECONDARY)
        self.pick_location_btn.pack(side="right")
        self.pos_label = ctk.CTkLabel(frame_pos, text="X:--- Y:---", font=self.value_font)
        self.pos_label.pack(side="right", padx=10)

        # --- Hotkey ---
        frame_hotkey = self._create_styled_frame(tab)
        frame_hotkey.grid(row=4, column=0, padx=10, pady=(20, 10), sticky="ew")
        self.hotkey_btn = ctk.CTkButton(frame_hotkey, text="Set Start/Stop Hotkey", font=self.main_font,
                                        command=lambda: self.logic.start_hotkey_binding('toggle_app'),
                                        fg_color=COLOR_PRIMARY, hover_color=COLOR_SECONDARY)
        self.hotkey_btn.pack(side="left")
        self.hotkey_label = ctk.CTkLabel(frame_hotkey, text=f"Current: {self.logic.hotkeys['toggle_app_str']}", font=self.main_font)
        self.hotkey_label.pack(side="left", padx=20)

    def _create_macro_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        
        # --- Controls ---
        frame_controls = self._create_styled_frame(tab)
        frame_controls.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.record_btn = ctk.CTkButton(frame_controls, text=f"Record ({self.logic.hotkeys['toggle_record_str']})",
                                        command=self.logic.toggle_recording, font=self.main_font,
                                        fg_color=COLOR_PRIMARY, hover_color=COLOR_SECONDARY)
        self.record_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.play_btn = ctk.CTkButton(frame_controls, text=f"Play ({self.logic.hotkeys['toggle_app_str']})", 
                                      command=lambda: self.logic.start_app('macro'), font=self.main_font,
                                      fg_color=COLOR_FOREGROUND, border_color=COLOR_SECONDARY, border_width=1)
        self.play_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.clear_btn = ctk.CTkButton(frame_controls, text="Clear", command=self.logic.engine.clear_macro, 
                                       font=self.main_font, fg_color=COLOR_FOREGROUND, border_color=COLOR_SECONDARY, 
                                       border_width=1)
        self.clear_btn.pack(side="left", expand=True, fill="x", padx=5)

        # --- Event Display ---
        self.macro_textbox = ctk.CTkTextbox(tab, state="disabled", font=self.mono_font,
                                            fg_color=COLOR_FOREGROUND, border_color=COLOR_SECONDARY, border_width=1)
        self.macro_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def update_cps_label(self, value):
        self.cps_value_label.configure(text=f"{float(value):.1f}")

    def update_hotkey_label(self, key_name, key_str):
        if key_name == 'toggle_app':
            self.hotkey_label.configure(text=f"Current: {key_str}")
        # Add logic for other hotkeys if needed

    def update_macro_display(self, events):
        self.macro_textbox.configure(state="normal")
        self.macro_textbox.delete("1.0", "end")
        if not events:
            self.macro_textbox.insert("1.0", "Record a sequence of clicks to begin.", ("italic",))
        else:
            for i, event in enumerate(events):
                delay_str = f"DELAY: {event['delay']:.2f}s".ljust(15)
                type_str = event['type'].upper().ljust(8)
                
                if event['type'] == 'click':
                    pos_str = f"@ ({event['pos'][0]}, {event['pos'][1]})"
                    details_str = f"{event['button'].name.upper()} {pos_str}"
                else: # 'move'
                    details_str = f"TO: ({event['pos'][0]}, {event['pos'][1]})"
                
                line = f"{i+1:03d} | {delay_str} | {type_str} | {details_str}\n"
                self.macro_textbox.insert("end", line)
        self.macro_textbox.configure(state="disabled")
