<div align="center">
  <img src="assets/logo.png" alt="Mushin Logo" width="100"/>
</div>

<a href="https://github.com/zanderooo/Mushin-Clicker">
  <img src="assets/header.svg" alt="Mushin (無心) - The art of effortless action."/>
</a>

<div align="center">
  <p>
    <a href="https://github.com/zanderooo/Mushin-Clicker/releases/latest">
      <img src="https://img.shields.io/github/v/release/zanderooo/Mushin-Clicker?style=for-the-badge&color=89B4FA&labelColor=1E1E2E&logo=github" alt="Latest Release">
    </a>
    <a href="https://github.com/zanderooo/Mushin-Clicker/actions/workflows/build.yml">
      <img src="https://img.shields.io/github/actions/workflow/status/zanderooo/Mushin-Clicker/build.yml?branch=main&style=for-the-badge&color=A6E3A1&labelColor=1E1E2E&logo=githubactions" alt="Build Status">
    </a>
    <a href="https://github.com/zanderooo/Mushin-Clicker/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/zanderooo/Mushin-Clicker?style=for-the-badge&color=F9E2AF&labelColor=1E1E2E" alt="License">
    </a>
  </p>
</div>

<div align="center">
  <img src="assets/screenshot.png" alt="Mushin Clicker Screenshot" width="700"/>
</div>

<div align="center">
  <img src="assets/divider.svg" />
</div>

In the pursuit of mastery, there is a state known as **Mushin (無心)** — a mind free from anger, fear, or ego. A mind without mind, where action becomes pure, effortless, and instinctual. This application is a tool built on that philosophy: to automate the mundane, so you can achieve a state of flow.

## ⇁ Features

| Feature                 | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| `✨` **Aesthetic UI**     | A clean, modern interface designed for clarity and focus.    |
| `🎚️` **Precision Control** | Fine-tune your Clicks Per Second with a smooth, responsive slider. |
| `🖱️` **Total Versatility** | Choose between Left, Right, or Middle mouse button operations. |
| `Hotkey Flow` **`F6`**   | A global hotkey to toggle clicking without ever leaving your active window. |

<div align="center">
  <img src="assets/divider.svg" />
</div>

## 🚀 Get Started

1.  Navigate to the [**Releases Page**](https://github.com/zanderooo/Mushin-Clicker/releases/latest).
2.  Download `Mushin.exe`.
3.  Run it. No installation needed.

> [!NOTE]
> Windows SmartScreen may show a warning as the app is not code-signed. This is standard for independent projects. Click `More info` → `Run anyway` to proceed.

<br>

<details>
<summary><div align="center"><code>BUILDING FROM SOURCE</code></div></summary>

<br>

```bash
# 1. Clone the repository
git clone https://github.com/zanderooo/Mushin-Clicker.git
cd Mushin-Clicker

# 2. Set up a virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python src/__main__.py