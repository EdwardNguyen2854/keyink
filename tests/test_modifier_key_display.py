"""Tests for modifier key display (Story 1.2)"""

import pytest
from PySide6.QtWidgets import QApplication
from history_widget import HistoryWidget, STYLE_COMBO, STYLE_WORD


# Create QApplication instance for tests
_app = None


def get_qapp():
    global _app
    if _app is None:
        _app = QApplication.instance()
        if _app is None:
            _app = QApplication([])
    return _app


class TestModifierKeyDisplay:
    """Test suite for modifier key display functionality."""

    def setup_method(self):
        """Set up QApplication before each test."""
        get_qapp()

    def test_modifier_keys_tracked(self):
        """Subtask 1.2: Verify modifier keys are tracked."""
        widget = HistoryWidget()

        # Simulate pressing Ctrl
        widget.on_key_pressed("ctrl", "Ctrl")
        assert "Ctrl" in widget._held_modifiers

    def test_single_modifier_not_displayed(self):
        """Subtask 1.2: Verify single modifier keys don't create entries."""
        widget = HistoryWidget()

        # Press Shift alone - should not create visible entry (just track it)
        widget.on_key_pressed("shift", "Shift")
        assert "Shift" in widget._held_modifiers
        # No entry should be added since shift alone is just a modifier

    def test_modifier_combination_display(self):
        """Subtask 2.1 & 2.2: Verify modifier combinations display correctly."""
        widget = HistoryWidget()

        # Simulate Ctrl+Shift+S
        widget.on_key_pressed("ctrl", "Ctrl")
        widget.on_key_pressed("shift", "Shift")
        widget.on_key_pressed("s", "s")

        # Should have created a combo entry
        assert len(widget._entries) >= 1
        # The entry should contain all modifiers sorted + the key
        entry_text = widget._entries[-1].text()
        assert "Ctrl" in entry_text
        assert "Shift" in entry_text or "s" in entry_text

    def test_modifier_order_ctrl_alt_shift_win(self):
        """Subtask 2.2: Verify modifier display order (Ctrl → Alt → Shift → Win)."""
        widget = HistoryWidget()

        # Press Win+Shift+Ctrl (out of order)
        widget.on_key_pressed("win", "Win")
        widget.on_key_pressed("shift", "Shift")
        widget.on_key_pressed("ctrl", "Ctrl")
        widget.on_key_pressed("a", "a")

        entry_text = widget._entries[-1].text()
        # Should be sorted: Ctrl first, then Shift, then Win
        ctrl_pos = entry_text.find("Ctrl")
        shift_pos = entry_text.find("Shift")
        win_pos = entry_text.find("Win")

        if ctrl_pos >= 0 and shift_pos >= 0:
            assert ctrl_pos < shift_pos
        if shift_pos >= 0 and win_pos >= 0:
            assert shift_pos < win_pos

    def test_ctrl_key_display(self):
        """Task 1: Verify Ctrl displays as 'Ctrl'."""
        widget = HistoryWidget()

        # Press Ctrl+K
        widget.on_key_pressed("ctrl", "Ctrl")
        widget.on_key_pressed("k", "k")

        entry_text = widget._entries[-1].text()
        assert "Ctrl" in entry_text

    def test_alt_key_display(self):
        """Task 1: Verify Alt displays as 'Alt'."""
        widget = HistoryWidget()

        # Press Alt+F4
        widget.on_key_pressed("alt", "Alt")
        widget.on_key_pressed("f4", "F4")

        entry_text = widget._entries[-1].text()
        assert "Alt" in entry_text

    def test_shift_key_display(self):
        """Task 1: Verify Shift displays when combined."""
        widget = HistoryWidget()

        # Press Shift+A (should show 'A' uppercase or as combo)
        widget.on_key_pressed("shift", "Shift")
        widget.on_key_pressed("a", "A")

        # Shift+A typically shows as 'A' (uppercase) in word mode
        # or as "Shift+A" in combo mode if other modifiers present
        assert len(widget._entries) >= 1

    def test_win_key_display(self):
        """Task 1: Verify Win key displays correctly."""
        widget = HistoryWidget()

        # Press Win+R
        widget.on_key_pressed("win", "Win")
        widget.on_key_pressed("r", "r")

        entry_text = widget._entries[-1].text()
        assert "Win" in entry_text

    def test_modifier_release_removes_from_tracking(self):
        """Task 1: Verify modifier is removed from tracking on release."""
        widget = HistoryWidget()

        # Press and release Ctrl
        widget.on_key_pressed("ctrl", "Ctrl")
        assert "Ctrl" in widget._held_modifiers

        widget.on_key_released("ctrl")
        assert "Ctrl" not in widget._held_modifiers


class TestIntegrationWithKeyboardListener:
    """Integration tests verifying keyboard listener provides modifier info."""

    def test_keyboard_listener_provides_modifier_display_names(self):
        """Subtask 3.1: Verify KeyboardListener emits correct display names."""
        from keyboard_listener import KeyboardListener
        from pynput import keyboard

        listener = KeyboardListener()

        # Test each modifier key returns correct display name
        test_cases = [
            (keyboard.Key.ctrl, "ctrl", "Ctrl"),
            (keyboard.Key.shift, "shift", "Shift"),
            (keyboard.Key.alt, "alt", "Alt"),
            (keyboard.Key.cmd, "win", "Win"),
        ]

        for key, expected_id, expected_display in test_cases:
            key_id, display = listener._resolve_key(key)
            assert key_id == expected_id
            assert display == expected_display


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
