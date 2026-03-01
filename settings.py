"""JSON-based settings persistence."""

import json
import os

_SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")

DEFAULTS = {
    "font_size": 24,
    "opacity": 88,
    "canvas_opacity": 100,
    "drawing_canvas_opacity": 15,
    "minimal_title_bar": False,
    "word_timeout_ms": 400,
    "show_special_keys": True,
    "drawing_hotkey": "alt+d",
}


def load_settings():
    """Load settings from JSON file, merged with defaults."""
    settings = dict(DEFAULTS)
    try:
        with open(_SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            settings.update(data)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return settings


def save_settings(data):
    """Write settings dict to JSON file."""
    with open(_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
