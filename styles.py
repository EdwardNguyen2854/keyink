"""Professional Minimal color constants.

Aesthetic: Clean, refined, unobtrusive
Mood: Premium, sophisticated, distraction-free
"""

import os
import json

_DARK_THEME = {
    "BG_COLOR": "#1a1a1a",
    "BG_SECONDARY": "#242424",
    "BG_TERTIARY": "#2d2d2d",
    "HISTORY_TEXT_COLOR": "#f0f0f0",
    "TITLE_COLOR": "#ffffff",
    "MUTED_TEXT": "#888888",
    "COMBO_HIGHLIGHT_COLOR": "#ffffff",
    "ACCENT_COLOR": "#888888",
    "ACCENT_DIM": "#666666",
    "SPECIAL_KEY_COLOR": "#999999",
    "SPECIAL_KEY_BG": "rgba(255, 255, 255, 0.05)",
    "MODIFIER_COLOR": "#777777",
    "MODIFIER_BG": "rgba(255, 255, 255, 0.03)",
    "BORDER_COLOR": "#333333",
    "BORDER_HIGHTLIGHT": "#444444",
    "CLOSE_BTN_COLOR": "#666666",
    "CLOSE_BTN_HOVER": "#ffffff",
    "CLOSE_BTN_SIZE": 20,
    "COMBO_BG": "rgba(128, 128, 128, 0.1)",
    "COMBO_BORDER": "rgba(128, 128, 128, 0.2)",
    "DROP_SHADOW": "0 8px 32px rgba(0, 0, 0, 0.4)",
    "SCROLLBAR_COLOR": "#444444",
    "SCROLLBAR_HOVER": "#666666",
    "FADE_DURATION_MS": 150,
    "FADE_OUT_DURATION_MS": 180,
}

_WHITE_THEME = {
    "BG_COLOR": "#ffffff",
    "BG_SECONDARY": "#f5f5f5",
    "BG_TERTIARY": "#ebebeb",
    "HISTORY_TEXT_COLOR": "#1a1a1a",
    "TITLE_COLOR": "#000000",
    "MUTED_TEXT": "#888888",
    "COMBO_HIGHLIGHT_COLOR": "#000000",
    "ACCENT_COLOR": "#555555",
    "ACCENT_DIM": "#777777",
    "SPECIAL_KEY_COLOR": "#666666",
    "SPECIAL_KEY_BG": "rgba(0, 0, 0, 0.05)",
    "MODIFIER_COLOR": "#555555",
    "MODIFIER_BG": "rgba(0, 0, 0, 0.03)",
    "BORDER_COLOR": "#e0e0e0",
    "BORDER_HIGHTLIGHT": "#cccccc",
    "CLOSE_BTN_COLOR": "#999999",
    "CLOSE_BTN_HOVER": "#000000",
    "CLOSE_BTN_SIZE": 20,
    "COMBO_BG": "rgba(85, 85, 85, 0.1)",
    "COMBO_BORDER": "rgba(85, 85, 85, 0.2)",
    "DROP_SHADOW": "0 8px 32px rgba(0, 0, 0, 0.1)",
    "SCROLLBAR_COLOR": "#cccccc",
    "SCROLLBAR_HOVER": "#aaaaaa",
    "FADE_DURATION_MS": 150,
    "FADE_OUT_DURATION_MS": 180,
}

_THEMES = {
    "dark": _DARK_THEME,
    "white": _WHITE_THEME,
}

def _load_theme():
    settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")
    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("theme", "dark")
    except (FileNotFoundError, json.JSONDecodeError):
        return "dark"

_current_theme = _load_theme()
_theme_data = _THEMES.get(_current_theme, _DARK_THEME)

BG_COLOR = _theme_data["BG_COLOR"]
BG_SECONDARY = _theme_data["BG_SECONDARY"]
BG_TERTIARY = _theme_data["BG_TERTIARY"]
HISTORY_TEXT_COLOR = _theme_data["HISTORY_TEXT_COLOR"]
TITLE_COLOR = _theme_data["TITLE_COLOR"]
MUTED_TEXT = _theme_data["MUTED_TEXT"]
COMBO_HIGHLIGHT_COLOR = _theme_data["COMBO_HIGHLIGHT_COLOR"]
ACCENT_COLOR = _theme_data["ACCENT_COLOR"]
ACCENT_DIM = _theme_data["ACCENT_DIM"]
SPECIAL_KEY_COLOR = _theme_data["SPECIAL_KEY_COLOR"]
SPECIAL_KEY_BG = _theme_data["SPECIAL_KEY_BG"]
MODIFIER_COLOR = _theme_data["MODIFIER_COLOR"]
MODIFIER_BG = _theme_data["MODIFIER_BG"]
BORDER_COLOR = _theme_data["BORDER_COLOR"]
BORDER_HIGHTLIGHT = _theme_data["BORDER_HIGHTLIGHT"]
CLOSE_BTN_COLOR = _theme_data["CLOSE_BTN_COLOR"]
CLOSE_BTN_HOVER = _theme_data["CLOSE_BTN_HOVER"]
CLOSE_BTN_SIZE = _theme_data["CLOSE_BTN_SIZE"]
COMBO_BG = _theme_data["COMBO_BG"]
COMBO_BORDER = _theme_data["COMBO_BORDER"]
DROP_SHADOW = _theme_data["DROP_SHADOW"]
SCROLLBAR_COLOR = _theme_data["SCROLLBAR_COLOR"]
SCROLLBAR_HOVER = _theme_data["SCROLLBAR_HOVER"]
FADE_DURATION_MS = _theme_data["FADE_DURATION_MS"]
FADE_OUT_DURATION_MS = _theme_data["FADE_OUT_DURATION_MS"]
