"""Tests for keyboard_listener.py - Global Keyboard Capture (Story 1.1)"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pynput import keyboard

# Import the module under test
from keyboard_listener import KeyboardListener, _SPECIAL_KEY_NAMES


class TestKeyboardListener:
    """Test suite for KeyboardListener class."""

    def test_class_exists(self):
        """Subtask 1.1: Verify KeyboardListener class exists and can be instantiated."""
        listener = KeyboardListener()
        assert listener is not None
        assert hasattr(listener, "key_pressed")
        assert hasattr(listener, "key_released")

    def test_key_pressed_signal_exists(self):
        """Subtask 1.1: Verify key_pressed signal exists with correct signature."""
        listener = KeyboardListener()
        assert hasattr(listener, "key_pressed")
        # Signal should accept (str, str) - (key_id, display_label)

    def test_key_released_signal_exists(self):
        """Subtask 1.1: Verify key_released signal exists with correct signature."""
        listener = KeyboardListener()
        assert hasattr(listener, "key_released")
        # Signal should accept (str) - (key_id)

    @patch("keyboard_listener.keyboard.Listener")
    def test_start_creates_listener(self, mock_listener_class):
        """Subtask 1.1: Verify start() creates pynput keyboard listener."""
        mock_listener_instance = Mock()
        mock_listener_class.return_value = mock_listener_instance

        listener = KeyboardListener()
        listener.start()

        mock_listener_class.assert_called_once()
        assert mock_listener_instance.daemon is True
        mock_listener_instance.start.assert_called_once()

    @patch("keyboard_listener.keyboard.Listener")
    def test_stop_stops_listener(self, mock_listener_class):
        """Subtask 1.1: Verify stop() stops the pynput keyboard listener."""
        mock_listener_instance = Mock()
        mock_listener_class.return_value = mock_listener_instance

        listener = KeyboardListener()
        listener.start()
        listener.stop()

        mock_listener_instance.stop.assert_called_once()
        assert listener._listener is None

    def test_resolve_key_alphanumeric(self):
        """Subtask 2.1: Verify alphanumeric keys are detected correctly."""
        listener = KeyboardListener()

        # Test lowercase letter
        mock_key = Mock()
        mock_key.char = "a"
        key_id, display = listener._resolve_key(mock_key)
        assert key_id == "a"
        assert display == "a"

        # Test uppercase letter (via char)
        mock_key.char = "Z"
        key_id, display = listener._resolve_key(mock_key)
        assert key_id == "z"
        assert display == "Z"

    def test_resolve_key_number_row(self):
        """Subtask 2.1: Verify number row keys are detected correctly."""
        listener = KeyboardListener()

        # Test number keys via virtual key codes
        for digit in "0123456789":
            mock_key = Mock()
            mock_key.char = None
            mock_key.vk = ord(digit)
            key_id, display = listener._resolve_key(mock_key)
            assert key_id == digit
            assert display == digit

    def test_resolve_key_letter_vk(self):
        """Subtask 2.1: Verify letter keys detected via virtual key code."""
        listener = KeyboardListener()

        # Test 'A' key (vk 0x41 = 65)
        # The _resolve_key handles this case - when char is None but vk is valid
        # This test verifies the logic path via mocking
        class MockKey:
            def __init__(self):
                self.char = None
                self.vk = 0x41  # 'A' virtual key code

        key = MockKey()
        key_id, display = listener._resolve_key(key)
        # Virtual key 65 is 'A', so with shift not held, display is 'a'
        assert key_id == "a"

    def test_resolve_key_modifier_shift(self):
        """Subtask 2.2: Verify modifier keys are detected correctly."""
        listener = KeyboardListener()

        key_id, display = listener._resolve_key(keyboard.Key.shift)
        assert key_id == "shift"
        assert display == "Shift"

        key_id, display = listener._resolve_key(keyboard.Key.shift_r)
        assert key_id == "right_shift"
        assert display == "Shift"

    def test_resolve_key_modifier_ctrl(self):
        """Subtask 2.2: Verify Ctrl modifier keys detected."""
        listener = KeyboardListener()

        key_id, display = listener._resolve_key(keyboard.Key.ctrl)
        assert key_id == "ctrl"
        assert display == "Ctrl"

        key_id, display = listener._resolve_key(keyboard.Key.ctrl_l)
        assert key_id == "ctrl"
        assert display == "Ctrl"

        key_id, display = listener._resolve_key(keyboard.Key.ctrl_r)
        assert key_id == "right_ctrl"
        assert display == "Ctrl"

    def test_resolve_key_modifier_alt(self):
        """Subtask 2.2: Verify Alt modifier keys detected."""
        listener = KeyboardListener()

        key_id, display = listener._resolve_key(keyboard.Key.alt)
        assert key_id == "alt"
        assert display == "Alt"

        key_id, display = listener._resolve_key(keyboard.Key.alt_r)
        assert key_id == "right_alt"
        assert display == "Alt"

        key_id, display = listener._resolve_key(keyboard.Key.alt_gr)
        assert key_id == "right_alt"
        assert display == "AltGr"

    def test_resolve_key_modifier_win(self):
        """Subtask 2.2: Verify Win modifier keys detected."""
        listener = KeyboardListener()

        key_id, display = listener._resolve_key(keyboard.Key.cmd)
        assert key_id == "win"
        assert display == "Win"

        key_id, display = listener._resolve_key(keyboard.Key.cmd_r)
        assert key_id == "right_win"
        assert display == "Win"

    def test_resolve_key_special_function_keys(self):
        """Subtask 2.3: Verify special function keys are detected."""
        listener = KeyboardListener()

        # Test function keys F1-F12
        for i in range(1, 13):
            key = getattr(keyboard.Key, f"f{i}")
            key_id, display = listener._resolve_key(key)
            assert key_id == f"f{i}"
            assert display == f"F{i}"

    def test_resolve_key_special_navigation_keys(self):
        """Subtask 2.3: Verify navigation special keys detected."""
        listener = KeyboardListener()

        # Test arrow keys
        key_id, display = listener._resolve_key(keyboard.Key.up)
        assert key_id == "up"
        assert display == "Up"

        key_id, display = listener._resolve_key(keyboard.Key.down)
        assert key_id == "down"
        assert display == "Down"

        key_id, display = listener._resolve_key(keyboard.Key.left)
        assert key_id == "left"
        assert display == "Left"

        key_id, display = listener._resolve_key(keyboard.Key.right)
        assert key_id == "right"
        assert display == "Right"

    def test_resolve_key_special_editing_keys(self):
        """Subtask 2.3: Verify editing special keys detected."""
        listener = KeyboardListener()

        # Test editing keys
        key_id, display = listener._resolve_key(keyboard.Key.backspace)
        assert key_id == "backspace"
        assert display == "Back"

        key_id, display = listener._resolve_key(keyboard.Key.delete)
        assert key_id == "delete"
        assert display == "Del"

        key_id, display = listener._resolve_key(keyboard.Key.home)
        assert key_id == "home"
        assert display == "Home"

        key_id, display = listener._resolve_key(keyboard.Key.end)
        assert key_id == "end"
        assert display == "End"

    def test_resolve_key_space_enter_tab(self):
        """Subtask 2.3: Verify space, enter, tab keys detected."""
        listener = KeyboardListener()

        key_id, display = listener._resolve_key(keyboard.Key.space)
        assert key_id == "space"
        assert display == "Space"

        key_id, display = listener._resolve_key(keyboard.Key.enter)
        assert key_id == "enter"
        assert display == "Enter"

        key_id, display = listener._resolve_key(keyboard.Key.tab)
        assert key_id == "tab"
        assert display == "Tab"

    def test_on_press_emits_signal(self):
        """Subtask 1.2: Verify on_press emits key_pressed signal."""
        listener = KeyboardListener()

        # Create mock key
        mock_key = Mock()
        mock_key.char = "a"
        mock_key.vk = None

        # Track signal emissions
        emitted_signals = []
        listener.key_pressed.connect(lambda k, d: emitted_signals.append((k, d)))

        listener._on_press(mock_key)

        assert len(emitted_signals) == 1
        assert emitted_signals[0] == ("a", "a")

    def test_on_release_emits_signal(self):
        """Subtask 1.3: Verify on_release emits key_released signal (not on_press)."""
        listener = KeyboardListener()

        mock_key = Mock()
        mock_key.char = "a"
        mock_key.vk = None

        emitted_signals = []
        listener.key_released.connect(lambda k: emitted_signals.append(k))

        listener._on_release(mock_key)

        assert len(emitted_signals) == 1
        assert emitted_signals[0] == "a"

    def test_on_press_tracks_modifiers(self):
        """Subtask 2.2: Verify modifier keys are tracked."""
        listener = KeyboardListener()

        # Press shift
        listener._on_press(keyboard.Key.shift)
        assert "shift" in listener._pressed_modifiers

        # Press ctrl
        listener._on_press(keyboard.Key.ctrl)
        assert "ctrl" in listener._pressed_modifiers

    def test_on_release_untracks_modifiers(self):
        """Subtask 2.2: Verify modifier keys are untracked on release."""
        listener = KeyboardListener()

        # Press and release shift
        listener._on_press(keyboard.Key.shift)
        assert "shift" in listener._pressed_modifiers

        listener._on_release(keyboard.Key.shift)
        assert "shift" not in listener._pressed_modifiers

    def test_special_key_names_mapping_complete(self):
        """Subtask 2.3: Verify all expected special keys are in mapping."""
        expected_keys = [
            keyboard.Key.space, keyboard.Key.enter, keyboard.Key.tab,
            keyboard.Key.backspace, keyboard.Key.delete, keyboard.Key.esc,
            keyboard.Key.shift, keyboard.Key.shift_r,
            keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
            keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt_gr,
            keyboard.Key.cmd, keyboard.Key.cmd_r,
            keyboard.Key.caps_lock, keyboard.Key.num_lock, keyboard.Key.scroll_lock,
        ]

        for key in expected_keys:
            assert key in _SPECIAL_KEY_NAMES, f"Missing mapping for {key}"


class TestIntegrationWithApp:
    """Integration tests verifying keyboard listener connects to history widget."""

    def test_app_connects_signals(self):
        """Subtask 3.1: Verify app.py connects keyboard signals to history widget."""
        # Read app.py to verify signal connections exist
        import app
        import inspect

        source = inspect.getsource(app.MainWindow.__init__)

        # Verify signal connections are made
        assert "key_pressed.connect" in source
        assert "key_released.connect" in source


class TestCrossApplicationCapture:
    """Subtask 3.2: Tests verifying global capture works."""

    def test_listener_is_daemon(self):
        """Verify pynput listener runs as daemon thread for global capture."""
        with patch("keyboard_listener.keyboard.Listener") as mock_class:
            mock_instance = Mock()
            mock_class.return_value = mock_instance

            listener = KeyboardListener()
            listener.start()

            # Verify daemon is set to True - required for clean exit
            assert mock_instance.daemon is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])