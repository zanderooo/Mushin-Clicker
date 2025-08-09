# Mushin Clicker

<p align="center">
  <img src="assets/logo.png" alt="Mushin Logo" width="150"/>
</p>

<p align="center">
  A clean, modern, and open-source auto-clicker.
</p>

---

**Mushin (無心)** - a mind without mind. A state where your actions are effortless and instinctual. This auto-clicker aims to automate repetitive tasks, letting you achieve a state of "mushin".

## ✨ Features

-   **Adjustable Speed:** Set Clicks Per Second (CPS) with a convenient slider.
-   **Button Selection:** Choose between left, right, or middle mouse buttons.
-   **Global Hotkey:** Start and stop clicking with the **F6** key, even when the app is minimized.
-   **Clean & Modern UI:** Built with simplicity and aesthetics in mind using CustomTkinter.
-   **Open-Source:** The entire codebase is available under the MIT License, open to contributions.

## 🚀 How to Use

1.  Go to the [**Releases**](https://github.com/zanderooo/Mushin-Clicker/releases) section of this repository.
2.  Download the latest version of `Mushin.exe`.
3.  Run the file and configure it to your needs.

*(Note: Since the application is not digitally signed, Windows SmartScreen might show a warning. Click "More info" and then "Run anyway" to proceed.)*

## 🛠️ Building from Source

If you want to build the application yourself:

1.  Clone the repository:
    ```bash
    git clone https://github.com/zanderooo/Mushin-Clicker.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd Mushin-Clicker
    ```
3.  Create and activate a virtual environment:
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Run the application:
    ```bash
    python src/__main__.py
    ```
6.  To build the `.exe` file, use the following command:
    ```bash
    pyinstaller --name Mushin --onefile --windowed --add-data "assets;assets" --icon="assets/icon.ico" src/__main__.py
    ```

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Made with ❤️ by zanderooo.