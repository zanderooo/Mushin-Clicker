<div align="center">
<pre>
+-----------------------------------------------------------------------------+
|                                                                             |
|    M U S H I N   / /   無 心                                                |
|                                                                             |
|    A state of no-mind. An instrument of flow.                               |
|                                                                             |
+-----------------------------------------------------------------------------+
</pre>
</div>

<div align="center">

[![Build Status](https://img.shields.io/github/actions/workflow/status/zanderooo/Mushin-Clicker/build.yml?branch=main&style=flat-square&color=A6E3A1&label=BUILD)](https://github.com/zanderooo/Mushin-Clicker/actions/workflows/build.yml)
[![Latest Release](https://img.shields.io/github/v/release/zanderooo/Mushin-Clicker?style=flat-square&color=89B4FA&label=RELEASE)](https://github.com/zanderooo/Mushin-Clicker/releases/latest)
[![License](https://img.shields.io/github/license/zanderooo/Mushin-Clicker?style=flat-square&color=F9E2AF&label=LICENSE)](https://github.com/zanderooo/Mushin-Clicker/blob/main/LICENSE)

</div>

```text
// C O N C E P T

Mushin is the martial arts term for a mind unburdened by thought or emotion,
focused only on the present action. This tool is a digital reflection of that
philosophy: a stateless, zero-configuration utility designed to eliminate
repetitive tasks and facilitate a state of uninterrupted workflow. It does
one thing, and it does it with precision.

// S Y S T E M   S P E C I F I C A T I O N S

┌──────────────────────────┬──────────────────────────────────────────────────┐
│ ATTRIBUTE                │ VALUE                                            │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ Version                  │ 1.0.0                                            │
│ License                  │ MIT                                              │
│ Author                   │ zanderooo                                        │
│ Core Technology          │ Python 3.10+                                     │
│ Interface                │ CustomTkinter                                    │
│ System Hook              │ Pynput                                           │
│ Global Hotkey            │ F6                                               │
│ Status                   │ Stable                                           │
└──────────────────────────┴──────────────────────────────────────────────────┘

// F E A T U R E   S E T

[+] DYNAMIC CPS CONTROL
    A fluid slider allows for precise adjustment of Clicks Per Second from
    1 to 100, updated in real-time.

[+] MOUSE BUTTON SELECTIVITY
    Full control over the click event source. Target the Left, Right,
    or Middle mouse button via a dropdown menu.

[+] GLOBAL HOTKEY ACTIVATION
    Toggle the clicker's state from any application using the F6 key.
    The process is system-wide, requiring no focus on the application window.

[+] STATELESS OPERATION
    Mushin writes no configuration files and leaves no trace on your system.
    Every session starts clean. What you see is what you get.

[+] CROSS-PLATFORM CORE
    Built with platform-agnostic libraries, ensuring the core logic is portable
    and ready for future expansion to other operating systems.

[+] ZERO-DEPENDENCY EXECUTABLE
    The final build is a single, self-contained .exe file that runs without
    any external dependencies or installation.

// O P E R A T I O N A L   P R O C E D U R E

1. Navigate to the [Releases] page of this repository.
2. Download the latest `Mushin.exe` binary.
3. Execute the file. No installation is required.
4. Configure parameters within the UI.
5. Press [F6] to activate or deactivate the process.

[Releases]: https://github.com/zanderooo/Mushin-Clicker/releases/latest


// B U I L D   P R O C E S S

For developers wishing to compile the application from source.

[1] CLONE REPOSITORY
    git clone https://github.com/zanderooo/Mushin-Clicker.git
    cd Mushin-Clicker

[2] PREPARE ENVIRONMENT (Windows)
    python -m venv venv
    .\venv\Scripts\activate

[3] INSTALL DEPENDENCIES
    pip install -r requirements.txt

[4] EXECUTE FROM SOURCE (for testing)
    python src/__main__.py

[5] COMPILE BINARY
    pyinstaller --name Mushin --onefile --windowed ^
    --add-data "assets;assets" --icon="assets/icon.ico" ^
    src/__main__.py

// C O R E   D E P E N D E N C I E S

┌───────────────────┬───────────┬─────────────────────────────────────────────┐
│ PACKAGE           │ VERSION   │ PURPOSE                                     │
├───────────────────┼───────────┼─────────────────────────────────────────────┤
│ customtkinter     │ 5.2.2     │ Modern graphical user interface toolkit     │
│ pynput            │ 1.7.6     │ System-wide input monitoring and control    │
│ Pillow            │ 10.3.0    │ Image processing for UI assets              │
│ PyInstaller       │ 6.15.0+   │ Executable bundler (developer dependency)   │
└───────────────────┴───────────┴─────────────────────────────────────────────┘


