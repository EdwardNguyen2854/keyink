"""Global keyboard hook using pynput, bridged to Qt signals."""

from PySide6.QtCore import QObject, Signal
from pynput import keyboard


# Map pynput special keys to display names
_SPECIAL_KEY_NAMES = {
    keyboard.Key.space: ("space", "Space"),
    keyboard.Key.enter: ("enter", "Enter"),
    keyboard.Key.tab: ("tab", "Tab"),
    keyboard.Key.backspace: ("backspace", "Back"),
    keyboard.Key.delete: ("delete", "Del"),
    keyboard.Key.esc: ("escape", "Esc"),
    keyboard.Key.shift: ("shift", "Shift"),
    keyboard.Key.shift_r: ("right_shift", "Shift"),
    keyboard.Key.ctrl: ("ctrl", "Ctrl"),
    keyboard.Key.ctrl_l: ("ctrl", "Ctrl"),
    keyboard.Key.ctrl_r: ("right_ctrl", "Ctrl"),
    keyboard.Key.alt: ("alt", "Alt"),
    keyboard.Key.alt_l: ("alt", "Alt"),
    keyboard.Key.alt_r: ("right_alt", "Alt"),
    keyboard.Key.alt_gr: ("right_alt", "AltGr"),
    keyboard.Key.cmd: ("win", "Win"),
    keyboard.Key.cmd_r: ("right_win", "Win"),
    keyboard.Key.caps_lock: ("caps_lock", "Caps"),
    keyboard.Key.num_lock: ("num_lock", "Num"),
    keyboard.Key.scroll_lock: ("scroll_lock", "Scroll"),
    keyboard.Key.print_screen: ("print_screen", "PrtSc"),
    keyboard.Key.pause: ("pause", "Pause"),
    keyboard.Key.insert: ("insert", "Ins"),
    keyboard.Key.home: ("home", "Home"),
    keyboard.Key.end: ("end", "End"),
    keyboard.Key.page_up: ("page_up", "PgUp"),
    keyboard.Key.page_down: ("page_down", "PgDn"),
    keyboard.Key.up: ("up", "Up"),
    keyboard.Key.down: ("down", "Down"),
    keyboard.Key.left: ("left", "Left"),
    keyboard.Key.right: ("right", "Right"),
    keyboard.Key.menu: ("menu", "Menu"),
}

# Add F1-F12
for i in range(1, 13):
    _key = getattr(keyboard.Key, f"f{i}", None)
    if _key:
        _SPECIAL_KEY_NAMES[_key] = (f"f{i}", f"F{i}")


class KeyboardListener(QObject):
    """Listens for global key events and emits Qt signals."""

    key_pressed = Signal(str, str)   # (key_id, display_label)
    key_released = Signal(str)       # (key_id)
    toggle_drawing = Signal()        # Ctrl+Shift+D pressed

    def __init__(self, parent=None):
        super().__init__(parent)
        self._listener = None
        self._pressed_modifiers = set()

    def start(self):
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        self._listener.daemon = True
        self._listener.start()

    def stop(self):
        if self._listener:
            self._listener.stop()
            self._listener = None

    def _resolve_key(self, key):
        """Return (key_id, display_label) for a pynput key."""
        if key in _SPECIAL_KEY_NAMES:
            return _SPECIAL_KEY_NAMES[key]

        if hasattr(key, "char") and key.char:
            ch = key.char
            key_id = ch.lower()
            display = ch
            return key_id, display

        if hasattr(key, "vk") and key.vk is not None:
            vk = key.vk
            # Number row 0-9
            if 0x30 <= vk <= 0x39:
                ch = chr(vk)
                return ch, ch
            # Letters A-Z
            if 0x41 <= vk <= 0x5A:
                ch = chr(vk).lower()
                shift_held = self._pressed_modifiers & {"shift", "right_shift"}
                display = ch.upper() if shift_held else ch
                return ch, display

        return str(key), str(key)

    def _on_press(self, key):
        key_id, display = self._resolve_key(key)
        if key_id in ("shift", "right_shift", "ctrl", "right_ctrl",
                       "alt", "right_alt", "win", "right_win"):
            self._pressed_modifiers.add(key_id)

        # Check for Ctrl+Shift+D to toggle drawing
        if key_id == "d":
            modifiers = self._pressed_modifiers
            if "ctrl" in modifiers or "right_ctrl" in modifiers:
                if "shift" in modifiers or "right_shift" in modifiers:
                    self.toggle_drawing.emit()

        self.key_pressed.emit(key_id, display)

    def _on_release(self, key):
        key_id, _ = self._resolve_key(key)
        self._pressed_modifiers.discard(key_id)
        self.key_released.emit(key_id)
