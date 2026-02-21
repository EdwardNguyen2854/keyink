"""Virtual keyboard visualization widget."""

from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PySide6.QtWidgets import QWidget

from styles import (
    KEY_DEFAULT_BG, KEY_DEFAULT_BORDER, KEY_PRESSED_BG,
    KEY_PRESSED_TEXT, KEY_TEXT_COLOR,
)

# Each row: list of (key_id, display_label, width_units)
# 1 unit = standard key width
KEYBOARD_LAYOUT = [
    # Row 0: Esc, F1-F12
    [
        ("escape", "Esc", 1), None,  # None = small gap
        ("f1", "F1", 1), ("f2", "F2", 1), ("f3", "F3", 1), ("f4", "F4", 1), None,
        ("f5", "F5", 1), ("f6", "F6", 1), ("f7", "F7", 1), ("f8", "F8", 1), None,
        ("f9", "F9", 1), ("f10", "F10", 1), ("f11", "F11", 1), ("f12", "F12", 1),
    ],
    # Row 1: Number row
    [
        ("`", "`", 1), ("1", "1", 1), ("2", "2", 1), ("3", "3", 1),
        ("4", "4", 1), ("5", "5", 1), ("6", "6", 1), ("7", "7", 1),
        ("8", "8", 1), ("9", "9", 1), ("0", "0", 1), ("-", "-", 1),
        ("=", "=", 1), ("backspace", "Back", 2),
    ],
    # Row 2: QWERTY
    [
        ("tab", "Tab", 1.5), ("q", "Q", 1), ("w", "W", 1), ("e", "E", 1),
        ("r", "R", 1), ("t", "T", 1), ("y", "Y", 1), ("u", "U", 1),
        ("i", "I", 1), ("o", "O", 1), ("p", "P", 1), ("[", "[", 1),
        ("]", "]", 1), ("\\", "\\", 1.5),
    ],
    # Row 3: ASDF
    [
        ("caps_lock", "Caps", 1.75), ("a", "A", 1), ("s", "S", 1), ("d", "D", 1),
        ("f", "F", 1), ("g", "G", 1), ("h", "H", 1), ("j", "J", 1),
        ("k", "K", 1), ("l", "L", 1), (";", ";", 1), ("'", "'", 1),
        ("enter", "Enter", 2.25),
    ],
    # Row 4: ZXCV
    [
        ("shift", "Shift", 2.25), ("z", "Z", 1), ("x", "X", 1), ("c", "C", 1),
        ("v", "V", 1), ("b", "B", 1), ("n", "N", 1), ("m", "M", 1),
        (",", ",", 1), (".", ".", 1), ("/", "/", 1), ("right_shift", "Shift", 2.75),
    ],
    # Row 5: Bottom row
    [
        ("ctrl", "Ctrl", 1.5), ("win", "Win", 1.25), ("alt", "Alt", 1.25),
        ("space", "Space", 6.25),
        ("right_alt", "Alt", 1.25), ("right_win", "Win", 1.25),
        ("menu", "Menu", 1.25), ("right_ctrl", "Ctrl", 1.5),
    ],
]

# Fade duration in ms
FADE_DURATION = 300
FADE_STEPS = 15


class KeyboardWidget(QWidget):
    """Draws a virtual keyboard and highlights pressed keys."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pressed_keys = {}  # key_id -> intensity (0.0 to 1.0)
        self._fade_timers = {}   # key_id -> QTimer
        self.setMinimumHeight(200)
        self.setMinimumWidth(700)

    def on_key_pressed(self, key_id, display_label):
        # Stop any ongoing fade for this key
        if key_id in self._fade_timers:
            self._fade_timers[key_id].stop()
            del self._fade_timers[key_id]
        self._pressed_keys[key_id] = 1.0
        self.update()

    def on_key_released(self, key_id):
        self._start_fade(key_id)

    def _start_fade(self, key_id):
        if key_id in self._fade_timers:
            self._fade_timers[key_id].stop()

        timer = QTimer(self)
        step = [0]

        def fade_step():
            step[0] += 1
            progress = step[0] / FADE_STEPS
            self._pressed_keys[key_id] = max(0.0, 1.0 - progress)
            if step[0] >= FADE_STEPS:
                timer.stop()
                self._pressed_keys.pop(key_id, None)
                self._fade_timers.pop(key_id, None)
            self.update()

        timer.timeout.connect(fade_step)
        timer.start(FADE_DURATION // FADE_STEPS)
        self._fade_timers[key_id] = timer

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Calculate key sizing
        padding = 8
        gap = 3
        row_gap = 4  # extra gap after function row

        # Total width units in widest row (row 1 has 15 units)
        max_units = 15.0
        usable_w = w - 2 * padding
        unit_w = (usable_w - (14 * gap)) / max_units  # approximate
        key_h = (h - 2 * padding - 5 * gap - row_gap) / len(KEYBOARD_LAYOUT)

        font = QFont("Segoe UI", max(8, int(key_h * 0.28)))
        painter.setFont(font)

        y = padding
        for row_idx, row in enumerate(KEYBOARD_LAYOUT):
            x = padding
            for item in row:
                if item is None:
                    x += unit_w * 0.25  # small gap
                    continue

                key_id, label, width_units = item
                kw = unit_w * width_units + gap * (width_units - 1)

                intensity = self._pressed_keys.get(key_id, 0.0)

                # Interpolate colors
                bg = self._lerp_color(KEY_DEFAULT_BG, KEY_PRESSED_BG, intensity)
                text_color = self._lerp_color(KEY_TEXT_COLOR, KEY_PRESSED_TEXT, intensity)
                border_color = self._lerp_color(KEY_DEFAULT_BORDER, KEY_PRESSED_BG, intensity)

                rect = QRectF(x, y, kw, key_h - 2)

                # Draw key background
                painter.setPen(QPen(QColor(border_color), 1))
                painter.setBrush(QBrush(QColor(bg)))
                painter.drawRoundedRect(rect, 4, 4)

                # Draw label
                painter.setPen(QColor(text_color))
                painter.drawText(rect, Qt.AlignCenter, label)

                x += kw + gap

            y += key_h
            if row_idx == 0:
                y += row_gap

        painter.end()

    @staticmethod
    def _lerp_color(c1_hex, c2_hex, t):
        """Linearly interpolate between two hex colors."""
        c1 = QColor(c1_hex)
        c2 = QColor(c2_hex)
        r = int(c1.red() + (c2.red() - c1.red()) * t)
        g = int(c1.green() + (c2.green() - c1.green()) * t)
        b = int(c1.blue() + (c2.blue() - c1.blue()) * t)
        return QColor(r, g, b).name()
