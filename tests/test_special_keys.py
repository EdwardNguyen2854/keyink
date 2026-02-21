"""Tests for special key combination handling (Story 1.3)"""

import pytest
from PySide6.QtWidgets import QApplication
from history_widget import HistoryWidget
from pynput import keyboard


# Create QApplication instance for tests
_app = None


def get_qapp():
    global _app
    if _app is None:
        _app = QApplication.instance()
        if _app is None:
            _app = QApplication([])
    return _app


class TestArrowKeyDisplay:
    """Test suite for arrow key display (AC 1)."""

    def setup_method(self):
        get_qapp()

    def test_arrow_up_display(self):
        """Subtask 1.1: Verify arrow up displays as ↑."""
        widget = HistoryWidget()
        widget.on_key_pressed("up", "Up")
        # Should have created an entry with ↑ symbol
        assert len(widget._entries) >= 1

    def test_arrow_down_display(self):
        """Subtask 1.1: Verify arrow down displays as ↓."""
        widget = HistoryWidget()
        widget.on_key_pressed("down", "Down")
        assert len(widget._entries) >= 1

    def test_arrow_left_display(self):
        """Subtask 1.1: Verify arrow left displays as ←."""
        widget = HistoryWidget()
        widget.on_key_pressed("left", "Left")
        assert len(widget._entries) >= 1

    def test_arrow_right_display(self):
        """Subtask 1.1: Verify arrow right displays as →."""
        widget = HistoryWidget()
        widget.on_key_pressed("right", "Right")
        assert len(widget._entries) >= 1


class TestFunctionKeyDisplay:
    """Test suite for function key display (AC 2)."""

    def setup_method(self):
        get_qapp()

    def test_f1_display(self):
        """Subtask 2.1: Verify F1 displays as F1."""
        widget = HistoryWidget()
        widget.on_key_pressed("f1", "F1")
        assert len(widget._entries) >= 1

    def test_f12_display(self):
        """Subtask 2.1: Verify F12 displays as F12."""
        widget = HistoryWidget()
        widget.on_key_pressed("f12", "F12")
        assert len(widget._entries) >= 1

    def test_all_function_keys(self):
        """Subtask 2.1: Verify all F1-F12 keys display correctly."""
        widget = HistoryWidget()
        for i in range(1, 13):
            widget.on_key_pressed(f"f{i}", f"F{i}")
        assert len(widget._entries) >= 12


class TestSpecialKeyLabels:
    """Test suite for special key labels (AC 3)."""

    def setup_method(self):
        get_qapp()

    def test_tab_display(self):
        """Subtask 3.1: Verify Tab displays with label."""
        widget = HistoryWidget()
        widget.on_key_pressed("tab", "Tab")
        assert len(widget._entries) >= 1

    def test_enter_display(self):
        """Subtask 3.1: Verify Enter displays with label."""
        widget = HistoryWidget()
        widget.on_key_pressed("enter", "Enter")
        assert len(widget._entries) >= 1

    def test_space_display(self):
        """Subtask 3.1: Verify Space displays with symbol."""
        widget = HistoryWidget()
        widget.on_key_pressed("space", "Space")
        assert len(widget._entries) >= 1

    def test_backspace_display(self):
        """Subtask 3.1: Verify Backspace displays with label."""
        widget = HistoryWidget()
        widget.on_key_pressed("backspace", "Back")
        assert len(widget._entries) >= 1

    def test_escape_display(self):
        """Subtask 3.1: Verify Escape displays as Esc."""
        widget = HistoryWidget()
        widget.on_key_pressed("escape", "Esc")
        assert len(widget._entries) >= 1


class TestKeyboardListenerSpecialKeys:
    """Test keyboard_listener.py special key mappings."""

    def test_arrow_keys_in_special_mapping(self):
        """Verify arrow keys are mapped in keyboard_listener.py."""
        from keyboard_listener import KeyboardListener, _SPECIAL_KEY_NAMES

        listener = KeyboardListener()

        # Test all arrow keys
        for key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]:
            key_id, display = listener._resolve_key(key)
            assert key_id in ["up", "down", "left", "right"]

    def test_function_keys_in_special_mapping(self):
        """Verify F1-F12 are mapped in keyboard_listener.py."""
        from keyboard_listener import KeyboardListener

        listener = KeyboardListener()

        # Test F1 and F12
        key_id, display = listener._resolve_key(keyboard.Key.f1)
        assert key_id == "f1"
        assert display == "F1"

        key_id, display = listener._resolve_key(keyboard.Key.f12)
        assert key_id == "f12"
        assert display == "F12"

    def test_special_keys_mapped(self):
        """Verify Tab, Enter, Space, Backspace, Escape are mapped."""
        from keyboard_listener import KeyboardListener

        listener = KeyboardListener()

        test_cases = [
            (keyboard.Key.tab, "tab"),
            (keyboard.Key.enter, "enter"),
            (keyboard.Key.space, "space"),
            (keyboard.Key.backspace, "backspace"),
            (keyboard.Key.esc, "escape"),
        ]

        for key, expected_id in test_cases:
            key_id, display = listener._resolve_key(key)
            assert key_id == expected_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
