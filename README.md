# KeyInk

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/UI-PySide6-31A8FF)](https://www.qt.io/qt-for-python)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

*A global keystroke overlay for demos, tutorials, and online training.*

---

## About

KeyInk displays your keystrokes as you type — perfect for:
- Online training and tutorials
- Software demos and walkthroughs
- Video recordings and screen captures
- Teaching or presenting

Built with Python and PySide6, KeyInk captures keyboard input system-wide and renders a clean, always-on-top overlay with grouped words, shortcuts, and annotations.

---

## Quick Facts

| | |
|---|---|
| **Task** | Desktop utility / Keystroke visualization |
| **Language** | Python 3.10+ |
| **Framework** | PySide6 |
| **Input** | Global keyboard events (pynput) |
| **Output** | On-screen keystroke overlay |
| **Status** | Usable |

---

## Features

- **Global key capture** — Works even when app is not focused
- **Always-on-top overlay** — Frameless, draggable window
- **Smart word grouping** — Groups keystrokes into words based on typing speed
- **Shortcut highlighting** — Shows combos like `Ctrl+C` distinctly
- **Drawing annotations** — Draw shapes, arrows, and annotations over your screen
- **Customizable** — Font size, opacity, colors, and more
- **System tray** — Runs quietly in background
- **Persistent settings** — Saves preferences automatically

---

## Installation

```bash
# Clone the repository
git clone https://github.com/EdwardNguyen2854/keyink.git
cd keyink

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

---

## Usage

### Controls

- **Drag** the window from any empty area to reposition
- **Right-click** for context menu (Settings, Toggle Drawing, Clear)
- **Minimize button** — Hide to tray
- **Close button** — Quit application

### Drawing Tools

Access drawing mode via:
- The **✏** button in the title bar
- Right-click menu → **Toggle Drawing**

Available tools:
- Pen (freehand)
- Rectangle
- Ellipse
- Arrow
- Line

### Settings

| Setting | Description |
|---------|-------------|
| Font size | Keystroke text size (px) |
| Window opacity | Background transparency (0-100%) |
| Canvas opacity | History panel transparency |
| Drawing opacity | Drawing overlay transparency |
| Word timeout | Time (ms) to group keystrokes into words |
| Show special keys | Display `Space`, `Enter`, `arrows`, etc. |

---

## Settings File

Located at `settings.json`:

```json
{
  "font_size": 24,
  "opacity": 88,
  "canvas_opacity": 100,
  "drawing_canvas_opacity": 15,
  "minimal_title_bar": false,
  "word_timeout_ms": 400,
  "show_special_keys": true
}
```

---

## Project Structure

```
keyink/
├── main.py              # Entry point
├── app.py               # Main window + tray + context menu
├── keyboard_listener.py # Global keyboard hook
├── history_widget.py    # Keystroke history rendering
├── drawing_canvas.py    # Drawing/annotation overlay
├── drawing_toolbar.py   # Drawing tools UI
├── settings_dialog.py   # Settings UI dialog
├── settings.py          # JSON persistence
├── styles.py           # Color/theme constants
├── keyboard_widget.py   # Virtual keyboard (optional)
└── tests/               # Test suite
```

---

## Limitations

- Requires keyboard access permissions (may need OS-level approval)
- Behavior may vary across operating systems
- Some protected/system contexts may block global hooks

---

## Privacy

KeyInk runs locally on your machine. It does **not** transmit any data to external servers.

---

## License

[MIT](LICENSE)
