import customtkinter as ctk
from PIL import Image
import os

class App(ctk.CTk):
    def __init__(self, clicker, toggle_callback, hotkey_str):
        super().__init__()

        self.clicker = clicker
        self.toggle_callback = toggle_callback # Callback function to toggle clicking from __main__
        self.hotkey_str = hotkey_str

        # --- Window Configuration ---
        self.title("Mushin Clicker")
        self.geometry("400x480")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Main Frame ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # --- Logo ---
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            logo_image = ctk.CTkImage(Image.open(logo_path), size=(100, 100))
            logo_label = ctk.CTkLabel(self.main_frame, image=logo_image, text="")
            logo_label.pack(pady=(10, 20))
        else:
            print(f"WARNING: logo.png not found in assets folder.")
            title_label = ctk.CTkLabel(self.main_frame, text="Mushin", font=ctk.CTkFont(size=40, weight="bold"))
            title_label.pack(pady=(30, 20))

        # --- CPS Controls ---
        cps_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cps_frame.pack(pady=10, padx=20, fill="x")
        
        cps_label_text = ctk.CTkLabel(cps_frame, text="Clicks Per Second (CPS):", font=ctk.CTkFont(size=14))
        cps_label_text.pack(side="left")

        self.cps_label_value = ctk.CTkLabel(cps_frame, text=f"{self.clicker.cps:.1f}", font=ctk.CTkFont(size=14, weight="bold"), width=40)
        self.cps_label_value.pack(side="right")

        self.cps_slider = ctk.CTkSlider(self.main_frame, from_=1, to=100, number_of_steps=99, command=self.update_cps)
        self.cps_slider.set(self.clicker.cps)
        self.cps_slider.pack(pady=(0, 20), padx=20, fill="x")

        # --- Mouse Button Selection ---
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=10, padx=20, fill="x")

        button_label = ctk.CTkLabel(button_frame, text="Mouse Button:", font=ctk.CTkFont(size=14))
        button_label.pack(side="left")

        self.button_combobox = ctk.CTkComboBox(button_frame, values=["Left", "Right", "Middle"], command=self.clicker.set_mouse_button)
        self.button_combobox.set("Left")
        self.button_combobox.pack(side="right", expand=True, fill="x")

        # --- Start/Stop Button ---
        self.toggle_button = ctk.CTkButton(self.main_frame, text=f"Start ({self.hotkey_str})", font=ctk.CTkFont(size=16, weight="bold"), command=self.toggle_callback, height=40)
        self.toggle_button.pack(pady=20, padx=20, fill="x")

        # --- Hotkey Information ---
        hotkey_info = ctk.CTkLabel(self.main_frame, text=f"Press {self.hotkey_str} to toggle clicking.", text_color="gray50", font=ctk.CTkFont(size=12))
        hotkey_info.pack(side="bottom", pady=10)

    def update_cps(self, value):
        """Updates the CPS label and passes the value to the clicker."""
        cps_value = float(value)
        self.cps_label_value.configure(text=f"{cps_value:.1f}")
        self.clicker.set_cps(cps_value)

    def update_button_state(self, is_clicking):
        """Updates the appearance of the Start/Stop button."""
        if is_clicking:
            self.toggle_button.configure(text=f"Stop ({self.hotkey_str})", fg_color="#D32F2F", hover_color="#B71C1C")
        else:
            self.toggle_button.configure(text=f"Start ({self.hotkey_str})", fg_color=("#3B8ED0", "#1F6AA5"), hover_color=("#36719F", "#144870"))