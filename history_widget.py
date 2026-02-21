"""Scrolling keystroke history — Professional Minimal aesthetic."""

import time

from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QGraphicsOpacityEffect,
    QSizePolicy,
)

from styles import (
    HISTORY_TEXT_COLOR, COMBO_HIGHLIGHT_COLOR, SPECIAL_KEY_COLOR,
    SPECIAL_KEY_BG, COMBO_BG, COMBO_BORDER,
    ACCENT_COLOR, FADE_DURATION_MS, FADE_OUT_DURATION_MS,
)

MAX_ENTRIES = 40
DEFAULT_WORD_TIMEOUT_MS = 400
DEFAULT_FONT_SIZE = 22

# Keys that are printable single characters
_PRINTABLE_KEYS = set("abcdefghijklmnopqrstuvwxyz0123456789")

# Special keys that break a word
_SPECIAL_DISPLAY = {
    "space", "enter", "tab", "backspace", "delete", "escape",
    "up", "down", "left", "right",
    "home", "end", "page_up", "page_down",
    "insert", "print_screen", "pause",
    "f1", "f2", "f3", "f4", "f5", "f6",
    "f7", "f8", "f9", "f10", "f11", "f12",
}

# Visual style types
STYLE_WORD = "word"
STYLE_COMBO = "combo"
STYLE_SPECIAL = "special"


def _build_styles(font_size=DEFAULT_FONT_SIZE):
    """Build minimal style definitions."""
    combo_size = max(12, font_size - 4)
    special_size = max(10, font_size - 6)
    return {
        STYLE_WORD: (
            f"color: {HISTORY_TEXT_COLOR}; "
            f"font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; "
            f"font-size: {font_size}px; font-weight: 400;"
            f"padding: 4px 8px; border-radius: 4px;"
        ),
        STYLE_COMBO: (
            f"color: {COMBO_HIGHLIGHT_COLOR}; "
            f"font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; "
            f"font-size: {combo_size}px; font-weight: 500;"
            f"padding: 4px 10px; border-radius: 4px; "
            f"background-color: {COMBO_BG};"
            f"border: 1px solid {COMBO_BORDER};"
        ),
        STYLE_SPECIAL: (
            f"color: {SPECIAL_KEY_COLOR}; "
            f"font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; "
            f"font-size: {special_size}px; font-weight: 400;"
            f"padding: 3px 8px; border-radius: 4px; "
            f"background-color: {SPECIAL_KEY_BG};"
        ),
    }


_STYLES = _build_styles()


class HistoryEntry(QLabel):
    """A single entry with fade-in animation."""

    def __init__(self, text, style_type=STYLE_WORD, parent=None, styles=None):
        super().__init__(text, parent)
        self.style_type = style_type
        s = styles or _STYLES
        self.setStyleSheet(s.get(style_type, s[STYLE_WORD]))
        self.setTextFormat(Qt.PlainText)
        self.setWordWrap(True)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Fade-in
        effect = QGraphicsOpacityEffect(self)
        effect.setOpacity(0.0)
        self.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(FADE_DURATION_MS)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        self._fade_anim = anim

    def update_text(self, text):
        self.setText(text)

    def fade_out_and_remove(self):
        """Fade out then delete."""
        effect = self.graphicsEffect()
        if not effect:
            self.deleteLater()
            return
        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(FADE_OUT_DURATION_MS)
        anim.setStartValue(effect.opacity())
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.InCubic)
        anim.finished.connect(self.deleteLater)
        anim.start()
        self._fade_anim = anim


class HistoryWidget(QWidget):
    """Shows scrolling list of keystrokes, grouping fast typing into words."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._entries = []
        self._current_word = ""
        self._current_entry = None
        self._last_key_time = 0
        self._word_timeout_ms = DEFAULT_WORD_TIMEOUT_MS
        self._font_size = DEFAULT_FONT_SIZE
        self._show_special_keys = True
        self._styles = _build_styles(self._font_size)
        self._flush_timer = QTimer(self)
        self._flush_timer.setSingleShot(True)
        self._flush_timer.timeout.connect(self._flush_word)

        self._modifier_keys = {
            "ctrl": "Ctrl", "right_ctrl": "Ctrl",
            "shift": "Shift", "right_shift": "Shift",
            "alt": "Alt", "right_alt": "Alt",
            "win": "Win", "right_win": "Win",
        }
        self._held_modifiers = set()

        # Layout
        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QWidget { background: transparent; }"
        )

        self._container = QWidget()
        self._container.setStyleSheet("background: transparent;")
        self._layout = QVBoxLayout(self._container)
        self._layout.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self._layout.setContentsMargins(4, 4, 4, 4)
        self._layout.setSpacing(4)

        self._scroll.setWidget(self._container)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._scroll)

    def on_key_pressed(self, key_id, display_label):
        now = time.time() * 1000

        # Track modifier state
        if key_id in self._modifier_keys:
            self._held_modifiers.add(self._modifier_keys[key_id])
            return

        # Check if only Shift is held
        non_shift_modifiers = self._held_modifiers - {"Shift"}

        # Is this printable?
        is_printable = key_id in _PRINTABLE_KEYS or (
            len(key_id) == 1 and key_id not in _SPECIAL_DISPLAY
        )

        # Modifier combo
        if non_shift_modifiers or (self._held_modifiers and not is_printable):
            self._flush_word()
            parts = sorted(self._held_modifiers) + [display_label]
            combo_str = "+".join(parts)
            self._add_entry(combo_str, style_type=STYLE_COMBO)
            self._last_key_time = now
            return

        if is_printable:
            elapsed = now - self._last_key_time
            if elapsed < self._word_timeout_ms and self._current_word:
                self._current_word += display_label
                if self._current_entry:
                    self._current_entry.update_text(self._current_word)
            else:
                self._flush_word()
                self._current_word = display_label
                self._current_entry = self._add_entry(
                    self._current_word, style_type=STYLE_WORD
                )

            self._last_key_time = now
            self._flush_timer.stop()
            self._flush_timer.start(self._word_timeout_ms)
        else:
            # Special key
            self._flush_word()

            if not self._show_special_keys:
                self._last_key_time = now
                return

            symbols = {
                "backspace": "⌫ Back",
                "space": "␣",
                "enter": "↵ Enter",
                "tab": "⇥ Tab",
                "escape": "Esc",
                "delete": "Del",
                "up": "↑", "down": "↓",
                "left": "←", "right": "→",
            }
            text = symbols.get(key_id, display_label)
            self._add_entry(text, style_type=STYLE_SPECIAL)
            self._last_key_time = now

    def on_key_released(self, key_id):
        if key_id in self._modifier_keys:
            self._held_modifiers.discard(self._modifier_keys[key_id])

    def _flush_word(self):
        self._flush_timer.stop()
        self._current_word = ""
        self._current_entry = None

    def _add_entry(self, text, style_type=STYLE_WORD):
        entry = HistoryEntry(text, style_type, self._container,
                             styles=self._styles)
        self._layout.addWidget(entry)
        self._entries.append(entry)

        # Remove oldest
        while len(self._entries) > MAX_ENTRIES:
            old = self._entries.pop(0)
            if old is self._current_entry:
                self._current_entry = None
                self._current_word = ""
            self._layout.removeWidget(old)
            old.fade_out_and_remove()

        QTimer.singleShot(10, self._scroll_to_bottom)
        return entry

    def _scroll_to_bottom(self):
        vbar = self._scroll.verticalScrollBar()
        vbar.setValue(vbar.maximum())

    def set_font_size(self, px):
        self._font_size = px
        self._styles = _build_styles(px)
        for entry in self._entries:
            entry.setStyleSheet(self._styles[entry.style_type])

    def set_show_special_keys(self, enabled):
        self._show_special_keys = enabled

    def set_word_timeout(self, ms):
        self._word_timeout_ms = ms

    def clear_history(self):
        self._flush_word()
        for entry in self._entries:
            self._layout.removeWidget(entry)
            entry.deleteLater()
        self._entries.clear()

    def set_opacity(self, opacity: int):
        """Set the opacity of the history widget (0-100)."""
        # Apply opacity to the scroll area's background
        alpha = int(opacity * 255 / 100)
        if opacity < 100:
            self._scroll.setStyleSheet(
                f"QScrollArea {{ border: none; background: rgba(0, 0, 0, {alpha}); }}"
                "QWidget { background: transparent; }"
            )
        else:
            self._scroll.setStyleSheet(
                "QScrollArea { border: none; background: transparent; }"
                "QWidget { background: transparent; }"
            )
